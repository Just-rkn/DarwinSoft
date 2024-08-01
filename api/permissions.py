from rest_framework import permissions

from tasks.models import TaskAccess


class IsAuthorOrHasTaskAccess(permissions.BasePermission):
    """
    Проверяет, является ли пользователь автором задачи или имеет к ней доступ.
    """

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True

        try:
            task_access = obj.accessible_users.get(user=request.user)
            if request.method in permissions.SAFE_METHODS:
                return task_access.access in ('read', 'update')
            if request.method.lower() in ('put', 'patch'):
                return task_access.access == 'update'
            return False
        except TaskAccess.DoesNotExist:
            return False
