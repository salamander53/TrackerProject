import requests
import hashlib
import bencode  # Đảm bảo thư viện này đã được cài đặt

# Địa chỉ của tracker
TRACKER_URL = 'http://48.210.50.194:8080/announce'

# Tạo dữ liệu giả cho yêu cầu
def generate_fake_data():
    info_hash = hashlib.sha1(b"fake_torrent_data").digest()  
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
            tracker_response = bencode.decode(response.content)
            print("Response from Tracker:", tracker_response)

           # Extracting the peer list from tracker response
            peers = tracker_response.get(b'peers', b'')
            peer_list = []

            # Ensure peers is not empty before parsing
            if peers:
                # Parsing compact peer list format (6 bytes per peer)
                for i in range(0, len(peers), 6):
                    ip = f"{peers[i]}.{peers[i + 1]}.{peers[i + 2]}.{peers[i + 3]}"
                    port = (peers[i + 4] << 8) + peers[i + 5]
                    
                    # Optionally, avoid adding self to peer list (replace 'your_public_ip' if needed)
                    if ip != 'your_public_ip' or port != 6881:  
                        peer_list.append({'ip': ip, 'port': port})

            # Print the parsed peer list
            print("Peer List:", peer_list)
    else:
        print("Failed to get a response:", response.status_code)

# Tạo dữ liệu giả và gửi yêu cầu
data = generate_fake_data()
send_announce_request(data)
