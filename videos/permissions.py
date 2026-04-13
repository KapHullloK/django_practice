from rest_framework import permissions


class VideoAccessPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj) -> bool:
        if obj.is_published:
            return True
        if request.user and request.user.is_staff:
            return True
        if request.user and request.user.is_authenticated:
            return obj.owner == request.user
        return False
