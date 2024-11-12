#import these two library
import bencodepy  #(install it before import it)
import hashlib

def calculate_info_hash(info):
    info_encoded = bencodepy.encode(info)  
    return hashlib.sha1(info_encoded).hexdigest()  

def info_command(file_content):
    try:
        print(file_content)
        data_torrent = bencodepy.decode(file_content)
        print(data_torrent)
        if not data_torrent or not isinstance(data_torrent, dict):
            raise ValueError("Invalid torrent structure")
        if 'info' not in data_torrent:
            raise ValueError("Missing 'info' field in torrent data")
        tracker_url = str(data_torrent.get('announce', ''))
        info_hash = calculate_info_hash(data_torrent['info'])
        piece_length = data_torrent['info'].get("piece length")
        pieces_buffer = data_torrent['info'].get('pieces')
        if not pieces_buffer or not isinstance(pieces_buffer, bytes) or len(pieces_buffer) % 20 != 0:
            raise ValueError("Invalid 'pieces' field in torrent data")
        pieces = [
            pieces_buffer[i:i + 20].hex() for i in range(0, len(pieces_buffer), 20)
        ]
        return {
            "trackerURL": tracker_url,
            "length": data_torrent['info'].get('length'),
            "infoHash": info_hash,
            "pieceLength": piece_length,
            "pieces": pieces,
        }
    except Exception as error:
        print("Error decoding torrent file:", error)
        raise ValueError("Failed to parse torrent file") from error
    
def read_torrent_file(file_path): 
    try: 
        with open(file_path, "rb") as file: 
            file_content = file.read() 
        return file_content 
    except Exception as e: 
        print(f"Error reading torrent file: {e}") 
        raise 
# Đường dẫn đến tệp torrent của bạn 
torrent_file_path = "test.torrent" 
# Đọc nội dung của tệp torrent 
file_content = read_torrent_file(torrent_file_path) 
# Gọi hàm info_command với nội dung của tệp torrent 
torrent_info = info_command(file_content) 
# In thông tin tệp torrent 
print("Torrent Info:",torrent_info)
