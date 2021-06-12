from django.urls import path
from .views import *

app_name = 'diary'
urlpatterns = [
    path('task-create/', TaskCreateAPIView.as_view(), name='task-create'),
    path('task-list/', TaskListAPIView.as_view(), name='task-list'),
    path('task-update/', TaskUpdadeAPIView.as_view(), name='task-update'),
    path('task-delete/', TaskDeleteAPIView.as_view(), name='task-delte'),
    path('task-list-preview/', TaskListPreviewAPIView.as_view(), name='task-list-preview')
]