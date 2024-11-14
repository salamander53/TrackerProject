from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import bencodepy
import time
import hashlib

# Lưu trữ torrent với danh sách peer (trong bộ nhớ)
torrents = {}
infoHash = hashlib.sha1(b"fake_torrent_data").hexdigest()
torrents[infoHash] = []

# Append each peer individually
torrents[infoHash].append({
    'ip': '100.0.0.1',  # IP mẫu
    'port': 6767,
    'peer_id': '123651263',
    'last_seen': time.time()
})

torrents[infoHash].append({
    'ip': '123.0.0.1',  # IP mẫu
    'port': 8787,
    'peer_id': '123432',
    'last_seen': time.time()
})

class TrackerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        if parsed_url.path == '/announce':
            self.AnnounceResponse(parsed_url)
        else:
            self.send_error(404, "Not Found")

    def AnnounceResponse(self, parsed_url):
        query = urllib.parse.parse_qs(parsed_url.query)
        
        info_hash = query.get('info_hash', [None])[0]
        peer_id = query.get('peer_id', [None])[0]
        port = query.get('port', [None])[0]
        ip = self.client_address[0]
        event = query.get('event', [None])[0]
        peerType = query.get('peerType', [None])[0]

        if info_hash:
            if peerType == 'leecher':
                peer_list = self.get_peers(info_hash)
                compact_peer_list = bytes(self.compact_peers(peer_list))
                self.CheckClientInfo(info_hash, peer_id, ip, port)
                # Chuyển các khóa sang bytes
                response = {
                    b'interval': 1800,
                    b'peers': compact_peer_list,
                }
            else:
                self.CheckTorrentInfo(info_hash)
                self.CheckClientInfo(info_hash, peer_id, ip, port)
                response = {
                    b'interval': 1800,
                }

            # Gửi phản hồi thành công
            self.send_response(200)
            self.send_header('Content-Type', 'application/x-bittorrent')
            self.end_headers()
            self.wfile.write(bencodepy.encode(response))
        else:
            # Gửi lỗi nếu thiếu tham số
            self.send_response(400)
            self.send_header('Content-Type', 'application/x-bittorrent')
            self.end_headers()
            self.wfile.write(bencodepy.encode({b'failure reason': b'Missing required parameters'}))

    def CheckClientInfo(self, info_hash, peer_id, ip, port):
        if info_hash not in torrents:
            torrents[info_hash] = []
        
        existing_peer = next((peer for peer in torrents[info_hash] if peer['peer_id'] == peer_id ), None)
        if existing_peer:
            existing_peer.update({'ip': ip, 'port': int(port), 'last_seen': time.time()})
        else:
            torrents[info_hash].append({
                'peer_id': peer_id,
                'ip': ip,
                'port': int(port),
                'last_seen': time.time()
            })

    def CheckTorrentInfo(self, info_hash):
        if info_hash not in torrents:
            torrents[info_hash] = []

    def get_peers(self, info_hash):
        return torrents.get(info_hash, [])

    def compact_peers(self, peer_list):
        # Chuyển đổi danh sách peer thành định dạng compact
        compact = bytearray()
        for peer in peer_list:
            ip_parts = map(int, peer['ip'].split('.'))
            compact.extend(bytearray(ip_parts))
            compact.extend(peer['port'].to_bytes(2, byteorder='big'))
        return compact
        
# Khởi động máy chủ
PORT = 8080
with HTTPServer(("", PORT), TrackerHandler) as httpd:
    print(f"BitTorrent tracker running on port {PORT}")
    httpd.serve_forever()