from django.db import models


class Video(models.Model):
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='videos'
    )
    name = models.CharField(max_length=255)
    is_published = models.BooleanField(default=False)
    total_likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class VideoFile(models.Model):
    class Quality(models.TextChoices):
        HD = "HD", "HD (720p)"
        FHD = "FHD", "FHD (1080p)"
        UHD = "UHD", "UHD (4K)"

    video = models.ForeignKey(
        'videos.Video',
        on_delete=models.CASCADE,
        related_name='video_files'
    )
    file = models.FileField(upload_to="videos/")
    quality = models.CharField(choices=Quality.choices)

    class Meta:
        unique_together = ('video', 'quality')

    def __str__(self):
        return f"{self.video.name} [{self.quality}]"


class Like(models.Model):
    video = models.ForeignKey(
        'videos.Video',
        on_delete=models.CASCADE,
        related_name='likes'
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='likes'
    )

    class Meta:
        unique_together = ('video', 'user')

    def __str__(self):
        return f"{self.user.username} → {self.video.name}"
