from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверка на права доступа для Админа или только чтение."""
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.is_admin
                or request.method in permissions.SAFE_METHODS)


class IsAdmin(permissions.BasePermission):
    """Проверка на права доступа для Админа."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAuthorOrModeratorOrReadOnly(permissions.BasePermission):
    """Проверка на права доступа для Модератора или Автора."""
    message = 'Пользователь не является автором.'
    safe_actions = ['list', 'create', 'retrieve']

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return (view.action in self.safe_actions
                or request.user.is_moderator
                or request.user.is_admin
                or request.user == obj.author)
