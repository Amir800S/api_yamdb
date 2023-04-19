from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка на права доступа для Админа."""
    def has_permission(self, request, view):
        return request.user.role == 'admin'
