import requests
import bencodepy
import hashlib
import os
import socket
import argparse

def calculate_info_hash(info):
    # Bencode hóa từ điển info và tính toán mã băm
    bencoded_info = bencodepy.encode(info)
    return hashlib.sha1(bencoded_info).digest()

def announce_to_tracker(torrent_data, port, peer_id):
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
        'ip': '192.168.1.3',  # Thay thế bằng IP công cộng nếu cần
    }

    try:
        response = requests.get(tracker_url, params=params)
        response.raise_for_status()  # Kiểm tra phản hồi có thành công không

        # Giải mã phản hồi bencoded từ tracker
        tracker_response = bencodepy.decode(response.content)

        if b"failure reason" in tracker_response:
            print("Thông báo đến tracker thất bại:", tracker_response[b"failure reason"].decode())
        else:
            print("Đã thông báo đến tracker thành công")
            return tracker_response

    except requests.RequestException as e:
        print("Lỗi khi thông báo đến tracker:", e)

    return None



def generate_torrent(file_path, announce_list, torrent_name):
    files = [os.path.abspath(file_path)]
    torrent_data = {
        "announce": announce_list[0],  # Chọn tracker đầu tiên
        "info": {
            "name": torrent_name,
            "length": os.path.getsize(file_path),
            "piece length": 16384,  # Kích thước mỗi phần (byte)
            "pieces": bencode_pieces(file_path, 16384)  # Tính toán các mã băm của từng phần
        }
    }

    # Tạo file torrent
    output_path = os.path.join("/tmp", f"{torrent_name}.torrent")
    with open(output_path, "wb") as torrent_file:
        torrent_file.write(bencodepy.encode(torrent_data))

    return output_path

def bencode_pieces(file_path, piece_length):
    """
    Tính toán mã băm SHA1 cho từng phần của file.

    Args:
        file_path (str): Đường dẫn đến file cần tính mã băm.
        piece_length (int): Kích thước mỗi phần (byte).

    Returns:
        bytes: Mã băm của từng phần.
    """
    pieces = bytearray()
    with open(file_path, "rb") as f:
        while True:
            piece = f.read(piece_length)
            if not piece:
                break
            pieces.extend(hashlib.sha1(piece).digest())
    return pieces

# Ví dụ sử dụng
if __name__ == "__main__":
    # Thay đổi đường dẫn và tên file theo nhu cầu
    file_path = "path/to/your/file"
    announce_list = ["http://example.com/announce"]
    torrent_name = "MyTorrent"

    torrent_file_path = generate_torrent(file_path, announce_list, torrent_name)
    print(f"Generated torrent file at: {torrent_file_path}")
def generate_peer_id():
    return os.urandom(20)
def read_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()
def send_handshake(conn, info_hash, peer_id):
    handshake = b'\x13BitTorrent protocol' + info_hash + peer_id
    conn.send(handshake)
def send_bitfield(conn, total_pieces):
    bitfield_length = (total_pieces + 7) // 8
    bitfield = bytearray([0xFF] * bitfield_length)  # All pieces available
    message = bytearray([0, 5]) + bitfield
    message_length = len(message)
    message = message[:2] + message_length.to_bytes(2, 'big') + message[2:]
    conn.send(message)
def send_unchoke(conn):
    message = bytearray([0, 1])
    message_length = len(message)
    message = message[:2] + message_length.to_bytes(2, 'big') + message[2:]
    conn.send(message)
def send_piece_message(conn, piece_index, begin, piece_data):
    message_length = 9 + len(piece_data)
    message = bytearray([0]) + message_length.to_bytes(4, 'big') + bytearray([7]) + piece_index.to_bytes(4, 'big') + begin.to_bytes(4, 'big') + piece_data
    conn.send(message)
def start_seeder(torrent_file, port=8180):
    file_content = read_file(torrent_file)
    torrent_data = bencodepy.decode(file_content)
    info_hash = calculate_info_hash(torrent_data[b'info'])
    piece_length = torrent_data[b'info'][b'piece length']
    file_length = torrent_data[b'info'][b'length']
    total_pieces = (file_length + piece_length - 1) // piece_length
    peer_id = generate_peer_id()

    # Announce to tracker on startup
    announce_to_tracker(torrent_data, port, peer_id)

    # Load the file into memory for simplicity
    file_path = os.path.join(os.getcwd(), torrent_data[b'info'][b'name'].decode())
    file_buffer = read_file(file_path)
    print(f"Starting seeder for file: {torrent_data[b'info'][b'name'].decode()}")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Seeder listening on port {port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection received from {addr}")
        buffer = bytearray()

        while True:
            data = conn.recv(4096)
            if not data:
                break
            buffer += data

            # Handshake processing
            if len(buffer) >= 68 and buffer[1:20] == b'BitTorrent protocol':
                print(f"Handshake received from {addr}")
                send_handshake(conn, info_hash, peer_id)
                send_bitfield(conn, total_pieces)
                send_unchoke(conn)

                buffer = buffer[68:]  # Remove handshake from buffer

            while len(buffer) >= 13:
                message_length = int.from_bytes(buffer[0:4], 'big')
                if len(buffer) < 4 + message_length:
                    break  # Wait for more data if incomplete
                
                message_id = buffer[4]
                if message_id == 6 and message_length == 13:  # Piece request
                    piece_index = int.from_bytes(buffer[5:9], 'big')
                    begin = int.from_bytes(buffer[9:13], 'big')
                    request_length = message_length - 9

                    print(f"Received request for piece {piece_index}, begin={begin}, length={request_length}")

                    piece_start = piece_index * piece_length + begin
                    piece_end = min(piece_start + request_length, len(file_buffer))
                    piece_data = file_buffer[piece_start:piece_end]

                    send_piece_message(conn, piece_index, begin, piece_data)

                buffer = buffer[4 + message_length:]  # Remove processed message

        conn.close()
        print(f"Connection closed: {addr}")
def main():
    parser = argparse.ArgumentParser(description="Torrent Seeder")
    parser.add_argument("command", help="Command to execute (e.g., 'seed')")
    parser.add_argument("torrent_file", help="Path to the torrent file")

    args = parser.parse_args()

    if args.command == "seed":
        start_seeder(args.torrent_file)
    else:
        print("Invalid command. Use 'seed' to start seeding.")

if __name__ == "__main__":
    main()