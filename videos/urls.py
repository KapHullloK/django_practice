from django.urls import path

from videos.views import VideoDetailView, VideoListView, VideoIdsView, LikeView, UsersLikesSubqueryListView, \
    UsersLikesGroupByListView

urlpatterns = [
    path("<int:pk>/", VideoDetailView.as_view()),
    path("", VideoListView.as_view()),
    path("ids/", VideoIdsView.as_view()),
    path("<int:pk>/likes/", LikeView.as_view()),
    path("statistics-subquery/", UsersLikesSubqueryListView.as_view()),
    path("statistics-group-by/", UsersLikesGroupByListView.as_view()),
]
