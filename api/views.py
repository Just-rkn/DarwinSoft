from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsAuthorOrHasTaskAccess
from api.serializers import TaskAccessSerializer, TaskSerializer
from tasks.models import Task, TaskAccess


class TaskViewsSet(viewsets.ModelViewSet):
    """ViewSet для управления задачами."""

    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.action == 'list':
            return (IsAuthenticated(),)
        return (IsAuthenticated(), IsAuthorOrHasTaskAccess())

    def get_queryset(self):
        if self.action == 'list':
            user = self.request.user
            return Task.objects.filter(
                Q(author=user) |
                Q(
                    accessible_users__user=user,
                    accessible_users__access__in=('read', 'update')
                )
            ).distinct()
        return Task.objects.all()


class TaskAccessView(APIView):
    """APIView для управления доступом к задачам."""

    def post(self, request, *args, **kwargs):
        serializer = TaskAccessSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        task_id = request.data.get('task')
        user_id = request.data.get('user')

        if not task_id or not user_id:
            return Response(
                {'detail': 'Поля task и user необходимо заполнить.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        task_access = get_object_or_404(TaskAccess, task=task_id, user=user_id)
        if task_access.task.author != request.user:
            return Response(
                {'detail': 'Только автор может изменять доступ.'},
                status=status.HTTP_403_FORBIDDEN
            )
        task_access.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
