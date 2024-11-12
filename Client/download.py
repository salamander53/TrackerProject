#import these two library
import bencodepy  #(install it before import it)
import hashlib

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
    info_encoded = bencodepy.encode(info)  
    return hashlib.sha1(info_encoded).hexdigest()  

def info_command(file_content):
    try:
        #print(file_content)
        data_torrent, _ = decode_bencode(file_content)
        #print(data_torrent)
        #if not data_torrent or not isinstance(data_torrent, dict):
        #    raise ValueError("Invalid torrent structure")
        #if 'info' not in data_torrent:
        #    raise ValueError("Missing 'info' field in torrent data")
        tracker_url = data_torrent.get('announce', '').decode()
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
            #"pieces": pieces,
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
