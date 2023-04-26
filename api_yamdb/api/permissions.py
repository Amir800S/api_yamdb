from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверка на права доступа для Админа или только для чтения."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.role == 'admin'))


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
        if hasattr(request.user, "role"):
            return (
                view.action in self.safe_actions
                or request.user.role == 'moderator'
                or request.user.role == 'admin'
                or request.user == obj.author
            )
        return view.action in self.safe_actions
