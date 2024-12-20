# import requests
# import bencodepy
# import bencode
# import hashlib
# import os
# import socket
# import argparse
# import signal 
# import sys
# import struct
# import math

# def decode_bencode(bencoded_value):
#     if chr(bencoded_value[0]).isdigit():
#         first_colon_index = bencoded_value.find(b":")
#         if first_colon_index == -1:
#             raise ValueError("Invalid encoded value")
#         length = int(bencoded_value[:first_colon_index])
#         return (
#             bencoded_value[first_colon_index + 1 : first_colon_index + 1 + length],
#             bencoded_value[first_colon_index + 1 + length :],
#         )
#     elif chr(bencoded_value[0]) == "i":
#         end_index = bencoded_value.find(b"e")
#         if end_index == -1:
#             raise ValueError("Invalid encoded value")
#         return int(bencoded_value[1:end_index]), bencoded_value[end_index + 1 :]
#     elif chr(bencoded_value[0]) == "l":
#         list_values = []
#         remaining = bencoded_value[1:]
#         while remaining[0] != ord("e"):
#             decoded, remaining = decode_bencode(remaining)
#             list_values.append(decoded)
#         return list_values, remaining[1:]
#     elif chr(bencoded_value[0]) == "d":
#         dict_values = {}
#         remaining = bencoded_value[1:]
#         while remaining[0] != ord("e"):
#             key, remaining = decode_bencode(remaining)
#             if isinstance(key, bytes):
#                 key = key.decode()
#             value, remaining = decode_bencode(remaining)
#             dict_values[key] = value
#         return dict_values, remaining[1:]
#     else:
#         raise NotImplementedError(
#             "Only strings, integers, lists, and dictionaries are supported at the moment"
#         )

# def calculate_info_hash(info):
#     # Bencode hóa từ điển info và tính toán mã băm
#     bencoded_info = bencodepy.encode(info)
#     return hashlib.sha1(bencoded_info).digest()

# def announce_to_tracker(torrent_data, port, peer_id, type):
#     info_hash = calculate_info_hash(torrent_data['info'])
#     tracker_url = torrent_data['announce']

#     params = {
#         'info_hash': info_hash.hex(),
#         'peer_id': peer_id,
#         'port': port,
#         'uploaded': 0,
#         'downloaded': 0,
#         'left': torrent_data['info']['length'],
#         'compact': 1,
#         'event': 'started',
#         'type': type,
#     }

#     try:
#         response = requests.get(tracker_url, params=params)
#         response.raise_for_status()  # Kiểm tra phản hồi có thành công không

#         # Giải mã phản hồi bencoded từ tracker
#         tracker_response = bencodepy.decode(response.content)

#         if b"failure reason" in tracker_response:
#             print("Thông báo đến tracker thất bại:", tracker_response[b"failure reason"].decode())
#         else:
#             print("Đã thông báo đến tracker thành công")
#             return tracker_response

#     except requests.RequestException as e:
#         print("Lỗi khi thông báo đến tracker:", e)

#     return None



# def generate_torrent(file_path, announce_list, torrent_name):
#     #files = [os.path.abspath(file_path)]
#     torrent_data = {
#         "announce": announce_list[0],  # Chọn tracker đầu tiên
#         "info": {
#             "name": torrent_name,
#             "length": os.path.getsize(file_path),
#             "piece length": 16384,  # Kích thước mỗi phần (byte)
#             "pieces": bytes(bencode_pieces(file_path, 16384))  # Tính toán các mã băm của từng phần
#         }
#     }

#     # Tạo file torrent
#     output_path = os.path.join("C:\\Users\\HP\\Downloads", f"{torrent_name}.torrent")
#     with open(output_path, "wb") as torrent_file:
#         torrent_file.write(bencodepy.encode(torrent_data))

#     return output_path

# def bencode_pieces(file_path, piece_length):
#     """
#     Tính toán mã băm SHA1 cho từng phần của file.

#     Args:
#         file_path (str): Đường dẫn đến file cần tính mã băm.
#         piece_length (int): Kích thước mỗi phần (byte).

#     Returns:
#         bytes: Mã băm của từng phần.
#     """
#     pieces = bytearray()
#     with open(file_path, "rb") as f:
#         while True:
#             piece = f.read(piece_length)
#             if not piece:
#                 break
#             pieces.extend(hashlib.sha1(piece).digest())
#     return pieces

# # Ví dụ sử dụng
# if __name__ == "__main__":
#     # Thay đổi đường dẫn và tên file theo nhu cầu
#     file_path = "C:/Users/HP/Downloads/Report.pdf"
#     # announce_list = ["http://48.210.50.194:8080/announce"]
#     announce_list = ["http://127.0.0.1:8080/announce"]
#     torrent_name = "MyTorrent"

#     torrent_file_path = generate_torrent(file_path, announce_list, torrent_name)
#     print(f"Generated torrent file at: {torrent_file_path}")
# def generate_peer_id():
#     return os.urandom(20)
# def read_file(file_path):
#     with open(file_path, 'rb') as f:
#         return f.read()
# def send_handshake(conn, info_hash, peer_id):
#     # handshake = b'\x13BitTorrent protocol' + info_hash + peer_id
#     # conn.send(handshake)
#     pstr = b"BitTorrent protocol"
#     pstrlen = len(pstr)
#     reserved = b'\x00' * 8
#     handshake = struct.pack('!B', pstrlen) + pstr + reserved + info_hash + peer_id
#     conn.send(handshake)

# def send_bitfield(conn, total_pieces):
#     # bitfield_length = (total_pieces + 7) // 8
#     # bitfield = bytearray([0xFF] * bitfield_length)  # All pieces available
#     # message = bytearray([0, 5]) + bitfield
#     # message_length = len(message)
#     # message = message[:2] + message_length.to_bytes(2, 'big') + message[2:]
#     # conn.send(message)

#     bitfield_length = (total_pieces + 7) // 8 
#     bitfield = bytearray([0xFF] * bitfield_length) # All pieces available 
#     bitfield_message = bytearray(4) + bytearray([5]) + bitfield 
#     struct.pack_into('!I', bitfield_message, 0, len(bitfield_message) - 4) 
#     print("Sent bitfield message") 
#     conn.send(bitfield_message)
# def send_unchoke(conn):
#     unchoke_message = bytearray(4 + 1)  # 4 bytes cho length và 1 byte cho ID
#     struct.pack_into('!I', unchoke_message, 0, 1)  # Ghi length (1)
#     unchoke_message[4] = 1  # Ghi ID (1)
    
#     print("Sent unchoke message")
#     # message = bytearray([0, 1])
#     # message_length = len(message)
#     # message = message[:2] + message_length.to_bytes(2, 'big') + message[2:]
#     conn.send(unchoke_message)
# def send_piece_message(conn, piece_index, begin, piece_data):
#     # message_length = 9 + len(piece_data)
#     # message = bytearray([0]) + message_length.to_bytes(4, 'big') + bytearray([7]) + piece_index.to_bytes(4, 'big') + begin.to_bytes(4, 'big') + piece_data
#     # conn.send(message)

#     message_length = 9 + len(piece_data)
#     piece_message = bytearray(4 + message_length)  # 4 bytes cho length

#     # Ghi length vào thông điệp
#     struct.pack_into('!I', piece_message, 0, message_length)
#     # Ghi ID (7 cho Piece)
#     piece_message[4] = 7
#     # Ghi piece index và begin offset
#     struct.pack_into('!I', piece_message, 5, piece_index)
#     struct.pack_into('!I', piece_message, 9, begin)
#     # Thêm dữ liệu thực tế
#     piece_message[13:] = piece_data
#     print(f"Sent piece message for piece {piece_index}, begin={begin}, length={len(piece_data)}")
#     conn.send(piece_message)
    
# def start_seeder(torrent_file, port=5050):
#     file_content = read_file(torrent_file)
#     torrent_data, _ = decode_bencode(file_content)
#     #torrent_data = bencodepy.decode(file_content)
#     info_hash = calculate_info_hash(torrent_data['info'])
#     piece_length = torrent_data['info']['piece length']
#     file_length = torrent_data['info']['length']
#     total_pieces = (file_length + piece_length - 1) // piece_length
#     peer_id = generate_peer_id()

#     # Announce to tracker on startup
#     announce_to_tracker(torrent_data, port, peer_id, 'seeder')
    
#     # Load the file into memory for simplicity
#     file_path = "C:/Users/HP/Downloads/Report.pdf"
#     #file_path = os.path.join(os.getcwd(), torrent_data['info']['name'].decode())
#     file_buffer = read_file(file_path)
#     print(f"Starting seeder for file: {torrent_data['info']['name'].decode()}")

#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind(('0.0.0.0', port))
#     server_socket.listen(5)
#     print(f"Seeder listening on port {port}")

#     def signal_handler(sig, frame): 
#         print('Shutting down server...') 
#         server_socket.close() # Đóng server socket 
#         sys.exit(0) 
#     signal.signal(signal.SIGINT, signal_handler)
#     # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
#     #     server_socket.bind(('0.0.0.0', port))
#     #     server_socket.listen(1)
#     #     print(f"Seeder is listening on {'0.0.0.0'}:{port}...")

#         # while True:
#         #     client_socket, addr = server_socket.accept()
#         #     print(f"Connection from {addr}")
#         #     data = client_socket.recv(1024).decode()
#         #     if data.startswith("START_TRANSFER"):
#         #         info_hash = data.split(":")[1]
#         #         print(f"Received START_TRANSFER for info_hash: {info_hash}")
#         #         # Bắt đầu gửi file hoặc thực hiện logic khác
#         #         # client_socket.close()
    
#     while True:
#         conn, addr = server_socket.accept()
#         print(f"Connection received from {addr}")
#         buffer = bytearray()

#         while True:
#             data = conn.recv(4096)
#             if not data:
#                 break
#             buffer += data
#             # Handshake processing
#             if len(buffer) >= 68 and buffer[1:20] == b'BitTorrent protocol':
#                 print(f"Handshake received from {addr}")
#                 send_handshake(conn, info_hash, peer_id)
#                 send_bitfield(conn, total_pieces)
#                 send_unchoke(conn)

#                 buffer = buffer[68:]  # Remove handshake from buffer

#             while len(buffer) >= 13:
#                 message_length = int.from_bytes(buffer[0:4], 'big')
#                 if len(buffer) < 4 + message_length:
#                     break  # Wait for more data if incomplete
                
#                 message_id = buffer[4]
#                 if message_id == 6 and message_length == 13:  # Piece request
#                     # piece_index = int.from_bytes(buffer[5:9], 'big')
#                     # begin = int.from_bytes(buffer[9:13], 'big')
#                     # request_length = message_length - 9
#                     piece_index = struct.unpack('>I', buffer[5:9])[0]  # Đọc piece index
#                     begin = struct.unpack('>I', buffer[9:13])[0]  # Đọc begin offset
#                     request_length = struct.unpack('>I', buffer[13:17])[0]  # Đọc độ dài yêu cầu

#                     print(f"Received request for piece {piece_index}, begin={begin}, length={request_length}")

#                     piece_start = piece_index * piece_length + begin
#                     piece_end = min(piece_start + request_length, len(file_buffer))
#                     piece_data = file_buffer[piece_start:piece_end]

#                     send_piece_message(conn, piece_index, begin, piece_data)

#                 buffer = buffer[4 + message_length:]  # Remove processed message

#         conn.close()
#         print(f"Connection closed: {addr}")

# def main():
#     parser = argparse.ArgumentParser(description="Torrent Seeder")
#     parser.add_argument("command", help="Command to execute (e.g., 'seed')")
#     parser.add_argument("torrent_file", help="Path to the torrent file")

#     args = parser.parse_args()

#     if args.command == "seed":
#         start_seeder(args.torrent_file)
#     else:
#         print("Invalid command. Use 'seed' to start seeding.")

# if __name__ == "__main__":
#     main()

import requests
import bencodepy
import bencode
import hashlib
import os
import socket
import argparse
import signal 
import sys
import struct
import math
import asyncio

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
    torrent_name_without_extension = os.path.splitext(torrent_name)[0]
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
    output_path = os.path.join("C:\\Users\\HP\\Downloads", f"{torrent_name_without_extension}.torrent")
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
    file_path = "C:/Users/HP/Downloads/Report.pdf"
    # announce_list = ["http://48.210.50.194:8080/announce"]
    announce_list = ["http://127.0.0.1:8080/announce"]
    #torrent_name = "MyTorrent"
    torrent_name = os.path.basename(file_path)
    
    torrent_file_path = generate_torrent(file_path, announce_list, torrent_name)
    print(f"Generated torrent file at: {torrent_file_path}")
def generate_peer_id():
    return os.urandom(20)
def read_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()
async def send_handshake(writer, info_hash, peer_id):
    # handshake = b'\x13BitTorrent protocol' + info_hash + peer_id
    # conn.send(handshake)
    pstr = b"BitTorrent protocol"
    pstrlen = len(pstr)
    reserved = b'\x00' * 8
    handshake = struct.pack('!B', pstrlen) + pstr + reserved + info_hash + peer_id
    # conn.send(handshake)
    writer.write(handshake)
    await writer.drain()


async def send_bitfield(writer, total_pieces):
    # bitfield_length = (total_pieces + 7) // 8
    # bitfield = bytearray([0xFF] * bitfield_length)  # All pieces available
    # message = bytearray([0, 5]) + bitfield
    # message_length = len(message)
    # message = message[:2] + message_length.to_bytes(2, 'big') + message[2:]
    # conn.send(message)

    bitfield_length = (total_pieces + 7) // 8 
    bitfield = bytearray([0xFF] * bitfield_length) # All pieces available 
    bitfield_message = bytearray(4) + bytearray([5]) + bitfield 
    struct.pack_into('!I', bitfield_message, 0, len(bitfield_message) - 4) 
    print("Sent bitfield message") 
    # conn.send(bitfield_message)
    writer.write(bitfield_message)
    await writer.drain()

async def send_unchoke(writer):
    unchoke_message = bytearray(4 + 1)  # 4 bytes cho length và 1 byte cho ID
    struct.pack_into('!I', unchoke_message, 0, 1)  # Ghi length (1)
    unchoke_message[4] = 1  # Ghi ID (1)
    
    print("Sent unchoke message")
    # message = bytearray([0, 1])
    # message_length = len(message)
    # message = message[:2] + message_length.to_bytes(2, 'big') + message[2:]
    # conn.send(unchoke_message)
    writer.write(unchoke_message)
    await writer.drain()
async def send_piece_message(writer, piece_index, begin, piece_data):
    # message_length = 9 + len(piece_data)
    # message = bytearray([0]) + message_length.to_bytes(4, 'big') + bytearray([7]) + piece_index.to_bytes(4, 'big') + begin.to_bytes(4, 'big') + piece_data
    # conn.send(message)

    message_length = 9 + len(piece_data)
    piece_message = bytearray(4 + message_length)  # 4 bytes cho length

    # Ghi length vào thông điệp
    struct.pack_into('!I', piece_message, 0, message_length)
    # Ghi ID (7 cho Piece)
    piece_message[4] = 7
    # Ghi piece index và begin offset
    struct.pack_into('!I', piece_message, 5, piece_index)
    struct.pack_into('!I', piece_message, 9, begin)
    # Thêm dữ liệu thực tế
    piece_message[13:] = piece_data
    print(f"Sent piece message for piece {piece_index}, begin={begin}, length={len(piece_data)}")
    # conn.send(piece_message)
    writer.write(piece_message)
    await writer.drain()
    
# async def start_seeder(torrent_file, reader, writer, port=5050):
#     file_content = read_file(torrent_file)
#     torrent_data, _ = decode_bencode(file_content)
#     #torrent_data = bencodepy.decode(file_content)
#     info_hash = calculate_info_hash(torrent_data['info'])
#     piece_length = torrent_data['info']['piece length']
#     file_length = torrent_data['info']['length']
#     total_pieces = (file_length + piece_length - 1) // piece_length
#     peer_id = generate_peer_id()

#     # Announce to tracker on startup
#     announce_to_tracker(torrent_data, port, peer_id, 'seeder')
    
#     # Load the file into memory for simplicity
#     file_path = "C:/Users/Do Truong Khoa/Downloads/Task1.pdf"
#     #file_path = os.path.join(os.getcwd(), torrent_data['info']['name'].decode())
#     file_buffer = read_file(file_path)
#     print(f"Starting seeder for file: {torrent_data['info']['name'].decode()}")

#     # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # server_socket.bind(('0.0.0.0', port))
#     # server_socket.listen(5)
#     # print(f"Seeder listening on port {port}")
#     addr = writer.get_extra_info('peername')
#     print(f"Connection received from {addr}")
#     async def signal_handler(sig, frame, writer): 
#         # print('Shutting down server...') 
#         # server_socket.close() # Đóng server socket 
#         # sys.exit(0) 
#         print(f"Connection closed: {addr}")
#         writer.close()
#         await writer.wait_closed()
#     server = await asyncio.start_server(start_seeder, '0.0.0.0', port)
#     async with server:
#         print(f"Seeder listening on port {port}")
#         await server.serve_forever()


#     signal.signal(signal.SIGINT, signal_handler)
#     # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
#     #     server_socket.bind(('0.0.0.0', port))
#     #     server_socket.listen(1)
#     #     print(f"Seeder is listening on {'0.0.0.0'}:{port}...")

#         # while True:
#         #     client_socket, addr = server_socket.accept()
#         #     print(f"Connection from {addr}")
#         #     data = client_socket.recv(1024).decode()
#         #     if data.startswith("START_TRANSFER"):
#         #         info_hash = data.split(":")[1]
#         #         print(f"Received START_TRANSFER for info_hash: {info_hash}")
#         #         # Bắt đầu gửi file hoặc thực hiện logic khác
#         #         # client_socket.close()
    
#     while True:
#         # conn, addr = server_socket.accept()
#         print(f"Connection received from {addr}")
#         buffer = bytearray()

#         while True:
#             # data = conn.recv(4096)
#             data = await reader.read(4096)
#             if not data:
#                 break
#             buffer += data
#             # Handshake processing
#             if len(buffer) >= 68 and buffer[1:20] == b'BitTorrent protocol':
#                 print(f"Handshake received from {addr}")
#                 send_handshake(writer, info_hash, peer_id)
#                 send_bitfield(writer, total_pieces)
#                 send_unchoke(writer)

#                 buffer = buffer[68:]  # Remove handshake from buffer

#             while len(buffer) >= 13:
#                 message_length = int.from_bytes(buffer[0:4], 'big')
#                 if len(buffer) < 4 + message_length:
#                     break  # Wait for more data if incomplete
                
#                 message_id = buffer[4]
#                 if message_id == 6 and message_length == 13:  # Piece request
#                     # piece_index = int.from_bytes(buffer[5:9], 'big')
#                     # begin = int.from_bytes(buffer[9:13], 'big')
#                     # request_length = message_length - 9
#                     piece_index = struct.unpack('>I', buffer[5:9])[0]  # Đọc piece index
#                     begin = struct.unpack('>I', buffer[9:13])[0]  # Đọc begin offset
#                     request_length = struct.unpack('>I', buffer[13:17])[0]  # Đọc độ dài yêu cầu

#                     print(f"Received request for piece {piece_index}, begin={begin}, length={request_length}")

#                     piece_start = piece_index * piece_length + begin
#                     piece_end = min(piece_start + request_length, len(file_buffer))
#                     piece_data = file_buffer[piece_start:piece_end]

#                     send_piece_message(writer, piece_index, begin, piece_data)

#                 buffer = buffer[4 + message_length:]  # Remove processed message

#         # conn.close()
#         print(f"Connection closed: {addr}")
#         writer.close()
#         await writer.wait_closed()

async def handle_client(reader, writer, info_hash, peer_id, total_pieces, piece_length, file_buffer):
    addr = writer.get_extra_info('peername')
    print(f"Connection received from {addr}")
    buffer = bytearray()

    while True:
        data = await reader.read(4096)
        if not data:
            break
        buffer += data

        # Xử lý handshake
        if len(buffer) >= 68 and buffer[1:20] == b'BitTorrent protocol':
            print(f"Handshake received from {addr}")
            await send_handshake(writer, info_hash, peer_id)
            await send_bitfield(writer, total_pieces)
            await send_unchoke(writer)
            buffer = buffer[68:]

        # Xử lý các thông điệp khác
        while len(buffer) >= 13:
            message_length = int.from_bytes(buffer[0:4], 'big')
            if len(buffer) < 4 + message_length:
                break

            message_id = buffer[4]
            if message_id == 6:  # Piece request
                piece_index = int.from_bytes(buffer[5:9], 'big')
                begin = int.from_bytes(buffer[9:13], 'big')
                request_length = int.from_bytes(buffer[13:17], 'big')

                print(f"Received request for piece {piece_index}, begin={begin}, length={request_length}")
                piece_start = piece_index * piece_length + begin
                piece_end = min(piece_start + request_length, len(file_buffer))
                piece_data = file_buffer[piece_start:piece_end]

                await send_piece_message(writer, piece_index, begin, piece_data)

            buffer = buffer[4 + message_length:]

    print(f"Connection closed: {addr}")
    writer.close()
    await writer.wait_closed()


async def start_seeder(torrent_file, port=5050):
    file_content = read_file(torrent_file)
    torrent_data, _ = decode_bencode(file_content)
    info_hash = calculate_info_hash(torrent_data['info'])
    piece_length = torrent_data['info']['piece length']
    file_length = torrent_data['info']['length']
    total_pieces = (file_length + piece_length - 1) // piece_length
    peer_id = generate_peer_id()

    # Load the file into memory
    file_path = "C:/Users/HP/Downloads/Report.pdf"
    file_buffer = read_file(file_path)

    # Announce to tracker
    announce_to_tracker(torrent_data, port, peer_id, 'seeder')
    print(f"Starting seeder for file: {torrent_data['info']['name'].decode()}")

    # Start the server
    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, info_hash, peer_id, total_pieces, piece_length, file_buffer),
        '0.0.0.0',
        port,
    )
    async with server:
        print(f"Seeder listening on port {port}")
        await server.serve_forever()


def main():
    parser = argparse.ArgumentParser(description="Torrent Seeder")
    parser.add_argument("command", help="Command to execute (e.g., 'seed')")
    parser.add_argument("torrent_file", help="Path to the torrent file")

    args = parser.parse_args()

    if args.command == "seed":
        asyncio.run(start_seeder(args.torrent_file))
    else:
        print("Invalid command. Use 'seed' to start seeding.")

if __name__ == "__main__":
    main()