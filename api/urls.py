from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import TaskViewsSet, TaskAccessView

router_v1 = DefaultRouter()
router_v1.register(r'tasks', TaskViewsSet, basename='task')

urlpatterns = [
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router_v1.urls)),
    path(
        'v1/task-access/', TaskAccessView.as_view(), name='taskaccess'
    )
]
