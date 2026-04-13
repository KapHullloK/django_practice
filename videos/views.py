from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from videos.models import Video
from videos.permissions import VideoAccessPermission
from videos.selectors import get_video_by_id, get_videos, get_videos_ids, get_published_video, get_users_likes_subquery, \
    get_users_likes_group_by
from videos.serializers import VideoSerializer, UserLikesSerializer
from videos.services import add_like, remove_like


class VideoDetailView(generics.RetrieveAPIView):
    serializer_class = VideoSerializer
    permission_classes = [VideoAccessPermission]

    def get_object(self):
        pk = self.kwargs["pk"]
        video = get_video_by_id(pk)
        self.check_object_permissions(self.request, video)
        return video


class VideoListView(generics.ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        return get_videos(self.request.user)


class VideoIdsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request) -> Response:
        ids = get_videos_ids()
        return Response(list(ids))


class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, pk: int) -> Response:
        try:
            video = get_published_video(pk)
        except Video.DoesNotExist:
            return Response({"detail": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
        added = add_like(video, request.user)
        if not added:
            return Response({"detail": "It's already been liked"}, status=status.HTTP_409_CONFLICT)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request: Request, pk: int) -> Response:
        video = get_published_video(pk)
        remove_like(video, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UsersLikesSubqueryListView(generics.ListAPIView):
    serializer_class = UserLikesSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return get_users_likes_subquery()


class UsersLikesGroupByListView(generics.ListAPIView):
    serializer_class = UserLikesSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return get_users_likes_group_by()
