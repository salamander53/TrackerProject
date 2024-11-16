from rest_framework import serializers
from torrents.models import Torrents

class TorrentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Torrents
        fields = ['title', 'announce', 'file_length', 'piece_length', 'pieces']

class TorrentRawDataSerializer(serializers.Serializer):
    raw_data = serializers.CharField()  # Lưu dữ liệu Bencode thô