from django.db.models import QuerySet, OuterRef, Sum, Subquery, IntegerField, F

from users.models import User
from videos.models import Video


def get_video_by_id(pk: int) -> Video:
    return (
        Video.objects
        .select_related("owner")
        .prefetch_related("video_files")
        .get(pk=pk)
    )


def get_videos(user: User) -> QuerySet:
    qs = (
        Video.objects
        .select_related("owner")
        .prefetch_related("video_files")
    )

    if user and user.is_staff:
        return qs.all()
    if user and user.is_authenticated:
        return qs.filter(is_published=True) | qs.filter(owner=user)
    return qs.filter(is_published=True)


def get_videos_ids() -> QuerySet:
    return (
        Video.objects
        .filter(is_published=True)
        .values_list("pk", flat=True)
    )


def get_published_video(pk: int) -> Video:
    return Video.objects.get(pk=pk, is_published=True)


def get_users_likes_subquery() -> QuerySet:
    likes_subquery = (
        Video.objects
        .filter(owner=OuterRef("pk"), is_published=True)
        .values("owner")
        .annotate(likes_sum=Sum("total_likes"))
        .values("likes_sum")
    )
    return (
        User.objects
        .annotate(likes_sum=Subquery(likes_subquery, output_field=IntegerField()))
        .order_by("-likes_sum")
        .values("username", "likes_sum")
    )


def get_users_likes_group_by() -> QuerySet:
    return (
        Video.objects
        .filter(is_published=True)
        .values("owner__username")
        .annotate(likes_sum=Sum("total_likes"), username=F("owner__username"), )
        .order_by("-likes_sum")
        .values("username", "likes_sum")
    )
