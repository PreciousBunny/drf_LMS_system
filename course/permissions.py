from users.models import UserRoles
from rest_framework import permissions


class UserPermissionsModerator(permissions.BasePermission):
    message = 'Вы не являетесь модератором!'

    def has_permission(self, request, view):
        if request.user.is_staff or request.user.role == UserRoles.MODERATOR and request.method in ['GET', 'PUT',
                                                                                                    'PATCH']:
            return True
        return False


class UserPermissionsOwner(permissions.BasePermission):
    message = 'Вы не являетесь владельцем!'

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner or request.user.is_superuser and request.method in ['GET', 'POST', 'PUT',
                                                                                         'PATCH', 'DELETE']:
            return True
        return False
