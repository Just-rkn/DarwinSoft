from rest_framework import serializers

from tasks.models import Task, TaskAccess, User


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Task."""

    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'author')


class TaskAccessSerializer(serializers.ModelSerializer):
    """Сериализатор для модели TaskAccess."""

    class Meta:
        model = TaskAccess
        fields = ('task', 'user', 'access')

    def validate_task(self, task):
        request = self.context['request']
        if not Task.objects.filter(id=task.id).exists():
            raise serializers.ValidationError('Задачи не существует.')
        if task.author != request.user:
            raise serializers.ValidationError(
                'Только автор может именять доступ.'
            )
        return task

    def validate_user(self, user):
        if not User.objects.filter(id=user.id).exists():
            raise serializers.ValidationError(
                'Такого пользователя не существует.'
            )
        return user
