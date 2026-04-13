from django.contrib import admin

from videos.models import VideoFile, Video


class VideoFileInline(admin.TabularInline):
    model = VideoFile
    extra = 1


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "is_published", "total_likes", "created_at"]
    list_filter = ["is_published"]
    search_fields = ["name", "owner__username"]
    readonly_fields = ["total_likes", "created_at"]
    inlines = [VideoFileInline]
