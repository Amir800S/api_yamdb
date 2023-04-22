from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and request.user.role == 'admin')


class IsAdmin(permissions.BasePermission):
    """Проверка на права доступа для Админа."""
    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin' or request.user.is_staff
