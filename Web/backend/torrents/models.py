from django.db import models

class Torrents(models.Model):
    created = models.DateTimeField(auto_now_add=True)  # Ngày tạo
    title = models.CharField(max_length=100, blank=True, default='')  # Tên file torrent
    announce = models.URLField()  # URL của tracker
    file_length = models.BigIntegerField()  # Kích thước file (byte)
    piece_length = models.IntegerField()  # Kích thước mỗi mảnh (byte)
    pieces = models.TextField()  # Dữ liệu băm của các mảnh (ở dạng hex)
    
    class Meta:
        ordering = ['created']
    
    def __str__(self):
        return self.title
