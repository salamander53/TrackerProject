from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from torrents.models import Torrents
from torrents.serializers import TorrentsSerializer
from django.http import JsonResponse
from .models import TorrentFile
from .duy_download import *
from .upload import *
# from .functional import info_command

@api_view(['GET', 'POST'])
def torrents_list(request, format=None):
    """
    List all code torrents, or create a new torrent.
    """
    if request.method == 'GET':
        torrents = Torrents.objects.all()
        serializer = TorrentsSerializer(torrents, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        torrent_file = request.FILES['file']

        # Lưu torrent file
        torrent_instance = TorrentFile.objects.create(file=torrent_file)
        torrent_path = torrent_instance.file.path

        start_leecher(torrent_path, "C:/Users/HP/Downloads/temp")

        # # Phân tích thông tin torrent
        # file_content = read_file(torrent_path)
        # torrent_data, _ = decode_bencode(file_content)
        
        # # Chuyển đổi các key từ bytes sang str
        # # torrent_data = convert_bytes_to_str(torrent_data)
        
        # tracker_url = torrent_data.get('announce', '')
        # peer_id = generate_peer_id()
        # peer_list = announce_to_tracker(torrent_data, 9999, peer_id, 'leecher')
        # print("Phần tử đầu tiên:", peer_list)

        # # Gửi tín hiệu tới Seeder trực tiếp
        # seeder_ip = '192.168.1.9'
        # seeder_port = 8180
        # info_hash = calculate_info_hash(torrent_data['info']).hex()

        # try:
        #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        #         sock.settimeout(5)
        #         sock.connect((seeder_ip, seeder_port))
        #         # message = f"START_TRANSFER:{info_hash}".encode()
        #         # sock.sendall(message)
        #         print(f"Sent START_TRANSFER signal to seeder {seeder_ip}:{seeder_port}")

        #     return Response({
        #         'message': 'Seeder notified and torrent created successfully',
        #     }, status=201)

        # except socket.error as e:
        #     return JsonResponse({'error': f'Error notifying Seeder: {str(e)}'}, status=500)
    
    return Response({
        'message': 'Downloaded successfully',
     }, status=201)


    

@api_view(['POST'])
def generate_torrent(request):
    """
    Nhận file từ request, tạo file torrent và khởi động seeder.
    """
    uploaded_file = request.FILES.get('file')
    
    if not uploaded_file:
        return JsonResponse({'error': 'No file uploaded'}, status=400)
    
    torrent_data = {
        "announce": announce_list[0],  # Chọn tracker đầu tiên
        "info": {
            "name": uploaded_file.name,
            "length": uploaded_file.size,
            "piece length": 16384,  # Kích thước mỗi phần (byte)
            "pieces": bytes(bencode_pieces(uploaded_file, 16384))  # Tính toán các mã băm của từng phần
        }
    }

    # Lưu file tải lên vào thư mục tạm
    temp_file_path = os.path.join("/tmp", uploaded_file.name)
    with open(temp_file_path, "wb") as torrent_file:
        torrent_file.write(bencodepy.encode(torrent_data))

    # Tạo file torrent
    # announce_list = ["http://48.210.50.194:8080/announce"]
    announce_list = ["http://127.0.0.1:8080/announce"]

    torrent_file_path = generate_torrent(temp_file_path, announce_list, uploaded_file.name)

    # Khởi động seeder
    start_seeder(torrent_file_path)

    return Response({
        'message': 'Torrent created and seeder started successfully',
        # 'torrentFilePath': torrent_file_path,
    }, status=201)

   

    
@api_view(['GET', 'PUT', 'DELETE'])
def torrents_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code torrent.
    """
    try:
        torrents = Torrents.objects.get(pk=pk)
    except Torrents.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TorrentsSerializer(torrents)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TorrentsSerializer(torrents, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        torrents.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)