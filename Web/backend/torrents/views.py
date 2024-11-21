from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from torrents.models import Torrents
from torrents.serializers import TorrentsSerializer
from django.http import JsonResponse
from .models import TorrentFile
from .duy_download import *
from .upload import *
from rest_framework.decorators import api_view, parser_classes 
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import threading
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
    
    return Response({
        'message': 'Downloaded successfully',
     }, status=201)

tasks_leech = {}
task_statuses = {}
def run_async_coroutine(coroutine, *args, **kwargs): asyncio.run(coroutine(*args, **kwargs))

async def start_leecher(torrent_file, output_path, task_id):
    file_content = read_file(torrent_file)
    await download_file(file_content, output_path)
    task_statuses[task_id] = "completed"

@method_decorator(csrf_exempt, name='dispatch')
class DownloadView(View):
    def post(self, request, *args, **kwargs):
        torrent_file = request.FILES['file']
        command = request.POST.get('command')
        path_output = request.POST.get('path_output')
        torrent_instance = TorrentFile.objects.create(file=torrent_file)
        torrent_path = torrent_instance.file.path
        if command == 'down':
            print("Received 'down' command")  # Thêm lệnh in để kiểm tra
            task_id = id(threading.current_thread())
            task_statuses[task_id] = "running"
            task = threading.Thread(target=run_async_coroutine, args=(start_leecher, torrent_path, path_output, task_id))
            task.start()
            tasks_leech[task_id] = task
            return JsonResponse({'message': 'Task started', 'task_id': task_id})

        elif command == 'stop':
            print("Received 'stop' command")  # Thêm lệnh in để kiểm tra
            task_id = int(request.POST.get('task_id'))
            task = tasks_leech.get(task_id)
            if task:
                print("Stopping thread is unsafe and not recommended")
                task_statuses[task_id] = "stopped"
                del tasks_leech[task_id]
                return JsonResponse({'message': 'Task stopped', 'task_id': task_id})
            else:
                return JsonResponse({'error': 'Task not found'}, status=404)

        return JsonResponse({'error': 'Invalid request'}, status=400)

@api_view(['GET']) 
def get_thread_status(request, task_id, format=None): 
    status = task_statuses.get(task_id, 'not found') 
    return Response({'task_id': task_id, 'status': status})

tasks_seed = {}
def run_async_coroutine(coroutine, *args, **kwargs): asyncio.run(coroutine(*args, **kwargs))

@method_decorator(csrf_exempt, name='dispatch')
class GenerateTorrentView(View):
    def post(self, request, *args, **kwargs):
        command = request.POST.get('command')
        path_input = request.POST.get('path_input')
        path_output = request.POST.get('path_output')

        if command == 'run':
            print("Received 'run' command")  # Thêm lệnh in để kiểm tra
            port = random.randint(1024, 65535) # Chọn một cổng ngẫu nhiên từ 1024 đến 65535
            task_id = id(threading.current_thread())
            task = threading.Thread(target=run_async_coroutine, args=(start_seeder, path_output, path_input, port))
            task.start()
            tasks_seed[task_id] = task
            return JsonResponse({'message': 'Task started', 'task_id': task_id})

        elif command == 'stop':
            print("Received 'stop' command")  # Thêm lệnh in để kiểm tra
            task_id = int(request.POST.get('task_id'))
            task = tasks_seed.get(task_id)
            if task:
                print("Stopping thread is unsafe and not recommended")
                del tasks_seed[task_id]
                return JsonResponse({'message': 'Task stopped', 'task_id': task_id})
            else:
                return JsonResponse({'error': 'Task not found'}, status=404)

        return JsonResponse({'error': 'Invalid request'}, status=400)


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