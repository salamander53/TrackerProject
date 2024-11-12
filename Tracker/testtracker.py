import requests
import hashlib
import bencodepy

# Địa chỉ của tracker
TRACKER_URL = 'http://48.210.50.194:8080/announce'
#TRACKER_URL = 'http://localhost:8080/announce'
# Tạo dữ liệu giả cho yêu cầu
def generate_fake_data():
    info_hash = hashlib.sha1(b"fake_torrent_data").hexdigest()
    peer_id = '-PC0001-' + ''.join(['%d' % (i % 10) for i in range(12)])  
    port = 6881
    uploaded = 0
    downloaded = 0
    left = 1000000  
    event = 'started' 
    peerType = 'leecher'
    return {
        'info_hash': info_hash,
        'peer_id': peer_id,
        'port': port,
        'uploaded': uploaded,
        'downloaded': downloaded,
        'left': left,
        'event': event,
        'peerType': peerType
    }

# Hàm gửi yêu cầu ANNOUNCE đến tracker
def send_announce_request(data):
    response = requests.get(TRACKER_URL, params=data)
    print("Status Code:", response.status_code)
    print("Headers:", response.headers)
    print("Content (raw):", response.content)
    
    if response.status_code == 200:
        try:
            # Giải mã phản hồi từ tracker
            tracker_response = bencodepy.decode(response.content)
            print("Response from Tracker:", tracker_response)
            
            # Trích xuất danh sách peers từ phản hồi tracker
            peers = tracker_response.get(b'peers', b'')
            peer_list = []
            
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
        
        except Exception as e:
            print("Failed to decode tracker response:", e)
    else:
        print("Failed to get a response:", response.status_code)

# Tạo dữ liệu giả và gửi yêu cầu
data = generate_fake_data()
send_announce_request(data)
