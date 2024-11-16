from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from torrents.models import Torrents
from torrents.serializers import TorrentsSerializer
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
        serializer = TorrentsSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
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