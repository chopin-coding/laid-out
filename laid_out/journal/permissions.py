from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow users to only see their own Journals.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
