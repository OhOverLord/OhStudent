from django.urls import path

from .views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView, RefreshTokenAPIView

app_name = 'account'
urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('refresh_token/', RefreshTokenAPIView.as_view(), name='refresh_token'),
]