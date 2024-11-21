import requests
import bencodepy
import bencode
import hashlib
import os
import socket
import argparse
import asyncio
import time
import struct
import aiofiles
import aiohttp
from typing import List, Dict, Any
import urllib.parse
import random
import tempfile
from pathlib import Path

def decode_bencode(bencoded_value):
    if chr(bencoded_value[0]).isdigit():
        first_colon_index = bencoded_value.find(b":")
        if first_colon_index == -1:
            raise ValueError("Invalid encoded value")
        length = int(bencoded_value[:first_colon_index])
        return (
            bencoded_value[first_colon_index + 1 : first_colon_index + 1 + length],
            bencoded_value[first_colon_index + 1 + length :],
        )
    elif chr(bencoded_value[0]) == "i":
        end_index = bencoded_value.find(b"e")
        if end_index == -1:
            raise ValueError("Invalid encoded value")
        return int(bencoded_value[1:end_index]), bencoded_value[end_index + 1 :]
    elif chr(bencoded_value[0]) == "l":
        list_values = []
        remaining = bencoded_value[1:]
        while remaining[0] != ord("e"):
            decoded, remaining = decode_bencode(remaining)
            list_values.append(decoded)
        return list_values, remaining[1:]
    elif chr(bencoded_value[0]) == "d":
        dict_values = {}
        remaining = bencoded_value[1:]
        while remaining[0] != ord("e"):
            key, remaining = decode_bencode(remaining)
            if isinstance(key, bytes):
                key = key.decode()
            value, remaining = decode_bencode(remaining)
            dict_values[key] = value
        return dict_values, remaining[1:]
    else:
        raise NotImplementedError(
            "Only strings, integers, lists, and dictionaries are supported at the moment"
        )

def calculate_info_hash(info):
    # Bencode hóa từ điển info và tính toán mã băm
    bencoded_info = bencodepy.encode(info)
    return hashlib.sha1(bencoded_info).digest()


async def get_public_ip() -> str:
    """Fetch the public IP address of the client."""
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.ipify.org?format=json") as response:
            data = await response.json()
            return data['ip']

async def announce_to_tracker(tracker_url: str, info_hash, file_length: int, peer_id: bytes, type, port=6060) -> List[Dict]:
    public_ip = await get_public_ip()

    params = urllib.parse.urlencode({
        'info_hash': info_hash.hex(), #bytes.fromhex(info_hash),
        'peer_id': peer_id,
        'port': port,
        'uploaded': 0,
        'downloaded': 0,
        'left': file_length,
        'compact': 1,
        'event': 'started',
        'type': type,
    })
    url = f"{tracker_url}?{params}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise ValueError(f"Tracker error: {response.status}")
            data = await response.read()
            decoded_response = bencodepy.decode(data)

            if b'failure reason' in decoded_response:
                raise ValueError(decoded_response[b'failure reason'].decode())

            peers = decoded_response[b'peers']
            return [
                {
                    'ip': f"{peers[i]}.{peers[i + 1]}.{peers[i + 2]}.{peers[i + 3]}",
                    'port': (peers[i + 4] << 8) + peers[i + 5],
                }
                for i in range(0, len(peers), 6)
                if f"{peers[i]}.{peers[i + 1]}.{peers[i + 2]}.{peers[i + 3]}" != "" #public_ip
            ]
'''
def announce_to_tracker(torrent_data, port, peer_id, type):
    info_hash = calculate_info_hash(torrent_data['info'])
    tracker_url = torrent_data['announce']

    params = {
        'info_hash': info_hash.hex(),
        'peer_id': peer_id,
        'port': port,
        'uploaded': 0,
        'downloaded': 0,
        'left': torrent_data['info']['length'],
        'compact': 1,
        'event': 'started',
        'type': type,
    }
    
    try:
        response = requests.get(tracker_url, params=params)
        response.raise_for_status()  # Kiểm tra phản hồi có thành công không
        peer_list = []
        # Giải mã phản hồi bencoded từ tracker
        tracker_response = bencodepy.decode(response.content)
        peers = tracker_response.get(b'peers', b'')
        
            
        # Đảm bảo rằng `peers` không rỗng trước khi phân tích
        if peers:
            # Phân tích danh sách peers dạng compact (6 byte cho mỗi peer)
            for i in range(0, len(peers), 6):
                ip = f"{peers[i]}.{peers[i + 1]}.{peers[i + 2]}.{peers[i + 3]}"
                port = (peers[i + 4] << 8) + peers[i + 5] 
                peer_list.append({'ip': ip, 'port': port})
            
        # In ra danh sách peers đã phân tích
        print("Peer List:", peer_list)
        
        if b"failure reason" in tracker_response:
            print("Thông báo đến tracker thất bại:", tracker_response[b"failure reason"].decode())
        else:
            print("Đã thông báo đến tracker thành công")
            return peer_list
        
    except requests.RequestException as e:
        print("Lỗi khi thông báo đến tracker:", e)
'''

def generate_peer_id():
    return os.urandom(20)
def read_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

async def download_piece(file_content, piece_index, output_path, peer, peer_id, work_queue):
    torrent_data,_ = decode_bencode(file_content)
    info_hash = calculate_info_hash(torrent_data['info'])
    print(f"Downloading piece {piece_index} from peer {peer['ip']}:{peer['port']}")

    piece_length = torrent_data['info']['piece length']
    last_piece_length = torrent_data['info']['length'] % piece_length or piece_length
    current_piece_length = last_piece_length if piece_index == (torrent_data['info']['length'] // piece_length) else piece_length
    # print(f"piece_length: {piece_length}" )
    # print(f"last_piece_length: {last_piece_length}" )
    # print(f"current_piece_length: {current_piece_length}" )
    reader, writer = await asyncio.open_connection(peer['ip'], peer['port'])
    keep_alive_interval = 30  # seconds
    handshake_msg = create_handshake(info_hash, peer_id)
    writer.write(handshake_msg)
    await writer.drain()
    async def keep_alive():
        while True:
            await asyncio.sleep(keep_alive_interval)
            writer.write(struct.pack('!I', 0))  # Send keep-alive message
            await writer.drain()

    asyncio.create_task(keep_alive())
    buffer = bytearray()
    received_length = 0
    requests_sent = 0
    block_size = 16 * 1024  # 16 KiB
    piece_data = bytearray(current_piece_length)
    bitfield_received = False
    peer_bitfield = bytearray()
    handshake_received = False

    def cleanup():
        if writer:
            writer.close()


    def send_request(begin, length):
        nonlocal requests_sent
        request_msg = struct.pack('>IBIII', 13, 6, piece_index, begin, length)
        writer.write(request_msg)
        requests_sent += 1

    def request_pieces():
        if not has_piece(piece_index):
            print(f"Peer doesn't have piece {piece_index}, skipping requests")
            return

        if piece_index in work_queue.completed_pieces: 
            print(f"Piece {piece_index} already downloaded, skipping requests") 
            return

        while requests_sent * block_size < current_piece_length:
            begin = requests_sent * block_size
            length = min(block_size, current_piece_length - begin)
            send_request(begin, length)

    def has_piece(index):
        byte_index = index // 8
        bit_index = 7 - (index % 8)
        return byte_index < len(peer_bitfield) and (peer_bitfield[byte_index] & (1 << bit_index)) != 0

    def handle_piece_message(payload):
        nonlocal received_length
        block_index = struct.unpack('>I', payload[:4])[0]
        block_begin = struct.unpack('>I', payload[4:8])[0]
        block_data = payload[8:]

        piece_data[block_begin:block_begin + len(block_data)] = block_data
        received_length += len(block_data)
        print(f"Download progress piece {piece_index}: {received_length / current_piece_length * 100:.2f}%")

        if received_length == current_piece_length:
            piece_hash = hashlib.sha1(piece_data).hexdigest()
            expected_hash = torrent_data['info']['pieces'][piece_index * 20: (piece_index + 1) * 20].hex()
            if piece_hash == expected_hash:
                with open(output_path, 'wb') as f:
                    f.write(piece_data)
                print(f"Piece {piece_index} downloaded successfully")
                cleanup()
            else:
                print(f"Piece {piece_index} hash mismatch")

    while True:
        data = await reader.read(4096)
        if not data:
            break
        buffer.extend(data)
        while len(buffer) >= 4:
            if not handshake_received:
                if buffer[1:20] == b'BitTorrent protocol':
                    handshake_received = True
                    print("Handshake received")
                    buffer = buffer[68:]  # Remove handshake
                    interested_msg = struct.pack('>IB', 1, 2)  # Interested message
                    writer.write(interested_msg)
                    await writer.drain()
                    print("Sent interested message")
                else:
                    break
            else:
                message_length = struct.unpack('>I', buffer[:4])[0]
                if len(buffer) < 4 + message_length:
                    break
                message_id = buffer[4]
                payload = buffer[5:5 + message_length]
                if message_id == 0:  # Choke
                    print("Choke received")
                elif message_id == 1:  # Unchoke
                    print("Unchoke received")
                    request_pieces()
                elif message_id == 5:  # Bitfield
                    peer_bitfield = payload
                    print("Bitfield received")
                elif message_id == 7:  # Piece
                    handle_piece_message(payload)
                else:
                    print(f"Unhandled message type: {message_id}")

                buffer = buffer[4 + message_length:]
    writer.close()
    await writer.wait_closed()
    return

def create_handshake(info_hash, peer_id):
    """Tạo thông điệp handshake."""
    pstr = b"BitTorrent protocol"
    pstrlen = len(pstr)
    reserved = b'\x00' * 8
    return struct.pack('!B', pstrlen) + pstr + reserved + info_hash + peer_id

class WorkQueue:
    """A queue to manage the download of pieces."""
    def __init__(self, total_pieces: int):
        self.pending_pieces = set(range(total_pieces))
        self.in_progress_pieces = set()
        self.completed_pieces = set()

    def get_next_piece(self) -> int:
        """Retrieve the next piece to download."""
        if not self.pending_pieces:
            return None
        piece = self.pending_pieces.pop()
        self.in_progress_pieces.add(piece)
        return piece

    def mark_piece_complete(self, piece_index: int):
        """Mark a piece as downloaded and verified."""
        self.in_progress_pieces.discard(piece_index)
        self.completed_pieces.add(piece_index)

    def is_complete(self) -> bool:
        """Check if all pieces are downloaded."""
        return not self.pending_pieces and not self.in_progress_pieces

"""
async def download_worker(peer, file_content: bytes, info_hash, peer_id: bytes, work_queue: WorkQueue, output_dir: str):
    
    while not work_queue.is_complete():
        piece_index = work_queue.get_next_piece()
        if piece_index is None:
            break
        try:
            # Implement downloading logic here
            mss = await download_piece(file_content, piece_index, output_dir, peer, peer_id, work_queue)
            # print(mss)
            pass
        except Exception as error:
            print(f"Failed to download piece {piece_index} from {peer['ip']}: {error}")
            #work_queue.mark_piece_failed(piece_index)      
"""

async def download_worker(peer, file_content, torrent_data, info_hash, peer_id, work_queue, downloaded_pieces, peers):

    max_retries = 50
    max_retries_per_piece = {}
    current_peer_index = peers.index(peer) if peer in peers else 0

    def get_next_peer():
        nonlocal current_peer_index
        current_peer_index = (current_peer_index + 1) % len(peers)
        return peers[current_peer_index]

    while not work_queue.is_complete():
        piece_index = work_queue.get_next_piece()
        if piece_index is None:
            print("No more pieces to download")
            break

        current_peer = peer
        retry_count = max_retries_per_piece.get(piece_index, 0)
        success = False

        while not success and retry_count < max_retries:
            try:
                temp_path = Path(os.path.join(
                    tempfile.gettempdir(),
                    f"piece_{piece_index}_{int(time.time())}_{random.randint(0, 10000)}"
                ))

                print(f"Attempting to download piece {piece_index} from peer {current_peer['ip']}:{current_peer['port']}")
                await download_piece(
                    file_content,
                    piece_index,
                    temp_path,
                    current_peer,
                    peer_id,
                    work_queue
                )

                if temp_path.exists():
                    with temp_path.open("rb") as temp_file:
                        piece_data = temp_file.read()
                        piece_hash = hashlib.sha1(piece_data).hexdigest()
                        expected_hash = torrent_data["info"]["pieces"][piece_index * 20: piece_index * 20 + 20].hex()

                        if piece_hash == expected_hash:
                            downloaded_pieces[piece_index] = piece_data
                            work_queue.mark_piece_complete(piece_index)
                            print(f"Piece {piece_index} verified and stored successfully")
                            success = True
                        else:
                            raise ValueError(f"Hash verification failed for piece {piece_index}")

                    temp_path.unlink()  # Xóa tệp tạm sau khi sử dụng

            except Exception as error:
                print(f"Error downloading piece {piece_index} from peer {current_peer['ip']}:{current_peer['port']}: {error}")

                if isinstance(error, ConnectionResetError):
                    print(f"Connection reset while downloading piece {piece_index}. Retrying...")
                    retry_count += 1
                    max_retries_per_piece[piece_index] = retry_count
                    current_peer = get_next_peer()
                    await asyncio.sleep(2)  
                else:
                    current_peer = get_next_peer()
                    max_retries_per_piece[piece_index] = retry_count + 1
                    await asyncio.sleep(1 * (retry_count + 1))  

        if not success:
            print(f"Failed to download piece {piece_index} after trying all peers")
            # work_queue.mark_piece_failed(piece_index)


async def download_file(file_content, output_path):
    torrent_data, _ = decode_bencode(file_content)
    info = torrent_data['info']
    file_length = info['length']
    piece_length = info['piece length']
    total_pieces = (file_length + piece_length - 1) // piece_length

    print(f"Downloading {total_pieces} pieces...")
    info_hash = calculate_info_hash(info)
    peer_id = generate_peer_id()
    tracker_url = torrent_data['announce'].decode()

    peers = await announce_to_tracker(tracker_url, info_hash, file_length, peer_id, "leecher")
    if not peers:
        raise ValueError("No peers found.")

    print(f"Found {len(peers)} peers.")
    downloaded_pieces = {}
    work_queue = WorkQueue(total_pieces)
    tasks = [
        download_worker(peer, file_content, torrent_data, info_hash, peer_id, work_queue, downloaded_pieces, peers)
        for peer in peers
    ]

    await asyncio.gather(*tasks)

    if work_queue.is_complete():
        print("Download complete.")
    else:
        print("Download incomplete. Some pieces are missing.")
    
    #final_data = b"".join(downloaded_pieces)
    final_data = b''.join(
        data for _, data in sorted(downloaded_pieces.items())
    )
    # Lấy tên tệp từ metadata
    file_name = torrent_data["info"]["name"]
    if isinstance(file_name, bytes):
        file_name = file_name.decode("utf-8")

    # Lưu tệp
    #output_path = Path(output_path) / file_name
    #output_path.parent.mkdir(parents=True, exist_ok=True)
    output_file_path = os.path.join(output_path, file_name)

            # Ensure the output directory exists
    Path(output_path).mkdir(parents=True, exist_ok=True)
    with open(output_file_path, "wb") as f:
        f.write(final_data)

    print(f"Download completed: {output_file_path}")
    return str(output_file_path)



async def start_leecher(torrent_file, output_path):
    file_content = read_file(torrent_file)
    await download_file(file_content, output_path)
    
    # torrent_data, _ = decode_bencode(file_content)
    # peer_id = generate_peer_id()
    # #peer_id = b'\x9c\xc3\xad\x9a\xe2\x15\x8f\xa5\xc4\xe9\x08\x7f\x5c\x84\xb6\x22\x92\x5b\x7a\x90'

    # # Announce to tracker on startup
    # peer_list = announce_to_tracker(torrent_data, port, peer_id, 'leecher')
    # print("Phần tử đầu tiên:", peer_list)
    # print(f"Starting leecher for file: {torrent_data['info']['name'].decode()}")
    # info_hash = calculate_info_hash(torrent_data['info'])
    # #server_socket 
    # ###
    # print(peer_list[0]['ip'], peer_list[0]['port'] )
    # asyncio.run(download_connection(info_hash, peer_list[0], peer_id,))

    
    ###
def main():
    parser = argparse.ArgumentParser(description="Torrent Leecher")
    parser.add_argument("command", help="Command to execute (e.g., 'leed')")
    parser.add_argument("torrent_file", help="Path to the torrent file")
    parser.add_argument("output_path", help="Path to the downloaded file")
    args = parser.parse_args()

    if args.command == "leech":
        start_leecher(args.torrent_file, args.output_path)
    else:
        print("Invalid command. Use 'leech' to start seeding.")

if __name__ == "__main__":
    main()