from django.urls import path
from . import views

urlpatterns = [
    path('track/<int:track_id>/', views.AudioTrackDetail.as_view(), name="track-api"),
    # path('genre/<int:id>/', views.GenreAPIView.as_view(), name='genre-api'),
    # path('tag/<int:id>/', views.TagAPIView.as_view(), name='tag-api'),
    path('playlist/<int:playlist_id>/', views.PlaylistDetail.as_view(), name='playlist-api'),
]
