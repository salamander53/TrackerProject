from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from torrents import views
from .views import torrents_list, notify_seeder

urlpatterns = [
    path('torrents/', views.torrents_list),
    path('torrents/<int:pk>/', views.torrents_detail),
    path('upload-torrent/', torrents_list, name='upload_torrent'),
    path('notify/', notify_seeder, name='notify'),
]

urlpatterns = format_suffix_patterns(urlpatterns)