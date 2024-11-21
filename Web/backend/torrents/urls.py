from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from torrents import views
from .views import DownloadView, GenerateTorrentView, get_thread_status

urlpatterns = [
    path('torrents/', views.torrents_list),
    path('torrents/<int:pk>/', views.torrents_detail),
    path('upload-torrent/', DownloadView.as_view(), name='upload_torrent'),
    # path('notify/', notify_seeder, name='notify'),
    path('generate_torrent/', GenerateTorrentView.as_view(), name='generate_torrent'),
    path('get-thread-status/<int:task_id>/', get_thread_status, name='get-thread-status'),
]

urlpatterns = format_suffix_patterns(urlpatterns)