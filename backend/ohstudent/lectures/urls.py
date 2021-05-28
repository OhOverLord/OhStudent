from django.urls import path
from .views import *

app_name = 'lectures'
urlpatterns = [
    path('<int:pk>', LectureDetailView.as_view(), name='lecture-detail'),
    path('delete/<int:pk>', LectureDeleteView.as_view(), name='lecture-delete'),
    path('create/', LectureCreateAPIView.as_view(), name='lecture-create'),
    path('update/<int:pk>', LectureUpdateView.as_view(), name='lecture-update'),
    path('lectures-list/', LecuresListView.as_view(), name='lectures-list')
]