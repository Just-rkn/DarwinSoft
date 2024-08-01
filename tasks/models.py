from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Task(models.Model):
    """Модель задачи."""

    title = models.CharField('Название', max_length=255)
    description = models.TextField('Текст')
    author = models.ForeignKey(
        User,
        related_name='tasks',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    access_users = models.ManyToManyField(
        User, related_name='accessible_tasks', through='TaskAccess'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class TaskAccess(models.Model):
    """Модель прав доступа к задаче."""

    class AccessType(models.TextChoices):
        """Типы доступа к задачам."""

        READ = 'read'
        UPDATE = 'update'

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='accessible_users',
        verbose_name='Задача'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    access = models.CharField(
        max_length=30, choices=AccessType.choices, verbose_name='Доступ'
    )

    def __str__(self):
        return f'Доступ {self.access} у {self.user} к {self.task}'

    class Meta:
        verbose_name = 'Доступ к задаче'
        verbose_name_plural = 'Доступ к задачам'
