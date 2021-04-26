from django.urls import path

from .views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView, RefreshTokenAPIView

app_name = 'account'
urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('user/', UserRetrieveUpdateAPIView.as_view(), name="user"),
    path('refresh_token/', RefreshTokenAPIView.as_view(), name='refresh_token'),
]
