from rest_framework import permissions


class IsUserProfile(permissions.BasePermission):
    """
    Класс запрещает действия над объектами, если пользователь не аутентифицирован.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.email == obj.email or request.user.is_superuser and request.method in ['GET', 'POST', 'PUT',
                                                                                               'DELETE']:
            return True
        return False
