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
    peer_list = []
    try:
        response = requests.get(tracker_url, params=params)
        response.raise_for_status()  # Kiểm tra phản hồi có thành công không

        # Giải mã phản hồi bencoded từ tracker
        tracker_response = bencodepy.decode(response.content)
        peers = tracker_response.get(b'peers', b'')
        
            
        # Đảm bảo rằng `peers` không rỗng trước khi phân tích
        if peers:
            # Phân tích danh sách peers dạng compact (6 byte cho mỗi peer)
            for i in range(0, len(peers), 6):
                ip = f"{peers[i]}.{peers[i + 1]}.{peers[i + 2]}.{peers[i + 3]}"
                port = (peers[i + 4] << 8) + peers[i + 5]
                
                # Tùy chọn: bỏ qua IP của chính bạn nếu cần
                # if ip != 'your_public_ip' or port != 6881:  
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

    

def generate_peer_id():
    return os.urandom(20)
def read_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

async def download_connection(info_hash, peer, peer_id):
    
    print(f"Downloading  from peer {peer['ip']}:{peer['port']}")

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

    handshake_received = False

    async def read_data():
        while True:
            data = await reader.read(1024)
            if not data:
                break

            if not handshake_received:
                if len(data) >= 68 and data[1:20].decode() == "BitTorrent protocol":
                    handshake_received = True
                    print("Handshake received")
                    writer.write(struct.pack('!B', 2))  # Send interested message
                    await writer.drain()
                continue

    await read_data()

def create_handshake(info_hash, peer_id):
    """Tạo thông điệp handshake."""
    pstr = b"BitTorrent protocol"
    pstrlen = len(pstr)
    reserved = b'\x00' * 8
    return struct.pack('!B', pstrlen) + pstr + reserved + info_hash + peer_id




def start_leecher(torrent_file, port=8180):
    file_content = read_file(torrent_file)
    torrent_data, _ = decode_bencode(file_content)
    #peer_id = generate_peer_id()
    peer_id = b'\x9c\xc3\xad\x9a\xe2\x15\x8f\xa5\xc4\xe9\x08\x7f\x5c\x84\xb6\x22\x92\x5b\x7a\x90'

    # Announce to tracker on startup
    peer_list = announce_to_tracker(torrent_data, port, peer_id, 'leecher')
    print("Phần tử đầu tiên:", peer_list)
    print(f"Starting leecher for file: {torrent_data['info']['name'].decode()}")
    info_hash = calculate_info_hash(torrent_data['info'])
    #server_socket 
    ###
    #asyncio.run(download_connection(info_hash, peer_list[0], peer_id,))
    
    ###
def main():
    parser = argparse.ArgumentParser(description="Torrent Leecher")
    parser.add_argument("command", help="Command to execute (e.g., 'leed')")
    parser.add_argument("torrent_file", help="Path to the torrent file")

    args = parser.parse_args()

    if args.command == "leech":
        start_leecher(args.torrent_file)
    else:
        print("Invalid command. Use 'leech' to start seeding.")

if __name__ == "__main__":
    main()