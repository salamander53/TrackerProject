from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from torrents import views

urlpatterns = [
    path('torrents/', views.torrents_list),
    path('torrents/<int:pk>/', views.torrents_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)