# tracks/serializers.py
from rest_framework import serializers
from tracks.models import AudioTrack
from playlists.models import PlaylistPage

class AudioTrackSerializer(serializers.ModelSerializer):

    audio_file_url = serializers.SerializerMethodField()
    track_image_url = serializers.SerializerMethodField()

    class Meta:
        model = AudioTrack
        fields = '__all__'

    def get_audio_file_url(self, obj):
        if obj.audio_file:
            return obj.audio_file.file.url
        return None

    def get_track_image_url(self, obj):
        if obj.track_image:  # Replace 'image' with the name of your image field.
            return obj.track_image.file.url  # Adjust this based on the structure of your image field.
        return None


class PlaylistSerializer(serializers.ModelSerializer):

    track_list = serializers.SerializerMethodField()
    track_details = serializers.SerializerMethodField()

    class Meta:
        model = PlaylistPage
        fields = '__all__'

    def get_track_list(self, obj):
        track_list = []
        if obj.body:
            for block in obj.body:  # Iterate through StreamChild objects
                block_data = block.value  # Access the value attribute of the StreamChild
                if 'page' in block_data:
                    track_list.append(block_data['page'].page_ptr_id)
        return track_list


    def get_track_details(self, obj):
        track_details = []
        if obj.body:
            for block in obj.body:
                block_data = block.value
                if 'page' in block_data:
                    track_id = block_data['page'].page_ptr_id
                    try:
                        audio_track = AudioTrack.objects.get(id=track_id)
                        serialized_track = AudioTrackSerializer(audio_track).data
                        track_details.append(serialized_track)
                    except AudioTrack.DoesNotExist:
                        # Handle the case when the AudioTrack is not found
                        pass
        return track_details
