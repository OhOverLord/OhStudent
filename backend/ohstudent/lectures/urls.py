from django.urls import path
from .views import *

app_name = 'lectures'
urlpatterns = [
    path('<int:pk>/', LectureDetailView.as_view(), name='lecture-detail'),
    path('delete/', LectureDeleteView.as_view(), name='lecture-delete'),
    path('create/', LectureCreateAPIView.as_view(), name='lecture-create'),
    path('update/', LectureUpdateView.as_view(), name='lecture-update'),
    path('share/', LectureShareView.as_view(), name='lecture-share'),
    path('lectures-list/', LecuresListView.as_view(), name='lectures-list')
]