from rest_framework import serializers

from videos.models import VideoFile, Video


class VideoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFile
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    video_files = VideoFileSerializer(many=True, read_only=True)

    class Meta:
        model = Video
        fields = ["id", "owner", "name", "total_likes", "created_at", "video_files"]


class UserLikesSerializer(serializers.Serializer):
    username = serializers.CharField()
    likes_sum = serializers.IntegerField()
