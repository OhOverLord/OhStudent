from django.urls import path
from .views import *

app_name = 'finance'
urlpatterns = [
    path('create/', WalletCreateAPIView.as_view(), name='wallet-create'),
    path('wallet-list/', WalletListAPIView.as_view(), name='wallet-list'),
    path('update/', WalletUpdateAPIView.as_view(), name='wallet-update'),
    path('delete/', WalletDeleteAPIView.as_view(), name='wallet-delete'),
]