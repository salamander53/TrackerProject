from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from torrents.models import Torrents
from torrents.serializers import TorrentsSerializer
from django.http import JsonResponse
from .models import TorrentFile
from .duy_download import *
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
        # serializer = TorrentsSerializer(data=request.data)
        # if serializer.is_valid():
        #     print(serializer.data)
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        torrent_file = request.FILES['file']

        # Lưu torrent file
        torrent_instance = TorrentFile.objects.create(file=torrent_file)
        torrent_path = torrent_instance.file.path

        # Phân tích thông tin torrent
        file_content = read_file(torrent_path)
        torrent_data, _ = decode_bencode(file_content)        
        tracker_url = torrent_data.get('announce', '').decode()
        peer_id = generate_peer_id()
        peer_list = announce_to_tracker(torrent_data, 9999, peer_id, 'leecher')
        print("Phần tử đầu tiên:", peer_list)

        # Gửi tín hiệu tới Seeder qua API notify_seeder
        seeder = peer_list[0]
        notify_payload = {
            'seeder_ip': '192.168.1.9',
            'seeder_port': 8180,
            'info_hash': calculate_info_hash(torrent_data['info']).hex(),
        }
        try:
            notify_response = requests.post('http://127.0.0.1:8000/notify/', json=notify_payload)
            if notify_response.status_code == 200:
                return JsonResponse({
                    'trackerurl': tracker_url,
                    'peers': peer_list,
                    'message': 'Seeder notified successfully',
                })
            else:
                return JsonResponse({
                    'trackerurl': tracker_url,
                    'message': 'Failed to notify Seeder',
                }, status=notify_response.status_code)
        except requests.RequestException as e:
            return JsonResponse({'error': f'Error notifying Seeder: {str(e)}'}, status=500)
    

@api_view(['POST'])
def notify_seeder(request):
    """
    API để thông báo seeder bắt đầu gửi file tới server.
    """
    seeder_ip = request.data.get('seeder_ip')
    seeder_port = request.data.get('seeder_port')
    info_hash = request.data.get('info_hash')
    print("posted to API notify_seeder")
    if not (seeder_ip and seeder_port ):
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    # Gửi tín hiệu tới seeder
    try:
        # Tạo kết nối TCP tới seeder
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((seeder_ip, int(seeder_port)))
            # message = f"START_TRANSFER:{info_hash}".encode()
            # sock.sendall(message)
            print(f"Sent START_TRANSFER signal to seeder {seeder_ip}:{seeder_port}")
            return JsonResponse({'message': 'Seeder notified successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


    
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