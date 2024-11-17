import requests
import bencodepy
import bencode
import hashlib
import os
import socket
import argparse

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
    #files = [os.path.abspath(file_path)]
    torrent_data = {
        "announce": announce_list[0],  # Chọn tracker đầu tiên
        "info": {
            "name": torrent_name,
            "length": os.path.getsize(file_path),
            "piece length": 16384,  # Kích thước mỗi phần (byte)
            "pieces": bytes(bencode_pieces(file_path, 16384))  # Tính toán các mã băm của từng phần
        }
    }

    # Tạo file torrent
    output_path = os.path.join("C:\\Users\\Do Truong Khoa\\Downloads", f"{torrent_name}.torrent")
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
    file_path = "C:/Users/Do Truong Khoa/Downloads/Task1.pdf"
    announce_list = ["http://48.210.50.194:8080/announce"]
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
    torrent_data, _ = decode_bencode(file_content)
    #torrent_data = bencodepy.decode(file_content)
    info_hash = calculate_info_hash(torrent_data['info'])
    piece_length = torrent_data['info']['piece length']
    file_length = torrent_data['info']['length']
    total_pieces = (file_length + piece_length - 1) // piece_length
    peer_id = generate_peer_id()

    # Announce to tracker on startup
    announce_to_tracker(torrent_data, port, peer_id, 'seeder')
    
    # Load the file into memory for simplicity
    file_path = "C:/Users/Do Truong Khoa/Downloads/Task1.pdf"
    #file_path = os.path.join(os.getcwd(), torrent_data['info']['name'].decode())
    file_buffer = read_file(file_path)
    print(f"Starting seeder for file: {torrent_data['info']['name'].decode()}")

    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket.bind(('0.0.0.0', port))
    # server_socket.listen(5)
    # print(f"Seeder listening on port {port}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen(1)
        print(f"Seeder is listening on {'0.0.0.0'}:{port}...")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            data = client_socket.recv(1024).decode()
            if data.startswith("START_TRANSFER"):
                info_hash = data.split(":")[1]
                print(f"Received START_TRANSFER for info_hash: {info_hash}")
                # Bắt đầu gửi file hoặc thực hiện logic khác
                # client_socket.close()
    
    """
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
    """
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