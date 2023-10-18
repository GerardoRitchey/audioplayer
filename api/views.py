from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tracks.models import AudioTrack
from playlists.models import PlaylistPage
from .serializers import AudioTrackSerializer, PlaylistSerializer
from django.http import Http404

class AudioTrackDetail(APIView):
    def get_object(self, track_id):
        try:
            return AudioTrack.objects.get(id=track_id)
        except AudioTrack.DoesNotExist:
            raise Http404

    def get(self, request, track_id, format=None):
        track = self.get_object(track_id)
        serializer = AudioTrackSerializer(track)
        return Response(serializer.data)


class PlaylistDetail(APIView):
    def get_object(self, playlist_id):
        try:
            return PlaylistPage.objects.get(id=playlist_id)
        except PlaylistPage.DoesNotExist:
            raise Http404

    def get(self, request, playlist_id, format=None):
        playlist = self.get_object(playlist_id)
        serializer = PlaylistSerializer(playlist)  # Replace PlaylistSerializer with your actual serializer
        return Response(serializer.data)


