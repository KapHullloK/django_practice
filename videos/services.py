from django.db.models import F

from users.models import User
from videos.models import Video, Like


def add_like(video: Video, user: User) -> bool:
    _, created = Like.objects.get_or_create(video=video, user=user)
    if created:
        Video.objects.filter(pk=video.pk).update(total_likes=F("total_likes") + 1)
    return created


def remove_like(video: Video, user: User) -> bool:
    deleted, _ = Like.objects.filter(video=video, user=user).delete()
    if deleted:
        Video.objects.filter(pk=video.pk).update(total_likes=F("total_likes") - 1)
        return True
    return False
