from django.urls import path
from .views import *

app_name = 'lectures'
urlpatterns = [
    path('<int:pk>/', LectureDetailView.as_view(), name='lecture-detail'),
    path('delete/', LectureDeleteView.as_view(), name='lecture-delete'),
    path('create/', LectureCreateAPIView.as_view(), name='lecture-create'),
    path('update/', LectureUpdateView.as_view(), name='lecture-update'),
    path('share/', LectureShareView.as_view(), name='lecture-share'),
    path('lectures-list/', LecuresListView.as_view(), name='lectures-list'),
    path('public-lecture-detail/', PublicLectureDetailView.as_view(), name='public-lecture-detail'),

    path('folder-create/', FolderCreateAPIView.as_view(), name='folder-create'),
    path('folder-list/', FolderListAPIView.as_view(), name='folder-create'),
    path('folder-update/', FolderUpdateAPIView.as_view(), name='folder-update'),
    path('folder-delete/', FolderDeleteAPIView.as_view(), name='folder-delete')
]