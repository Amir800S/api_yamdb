from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    message = 'Пользователь не является автором.'
    safe_actions = ['list', 'create', 'retrieve']

    def has_permission(self, request, obj):
        return (
            obj.action in self.safe_actions
            or request.user == obj.get_object().author
        )