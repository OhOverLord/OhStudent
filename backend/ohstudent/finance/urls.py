from django.urls import path
from .views import *


app_name = 'finance'
urlpatterns = [
    path('wallet-create/', WalletCreateAPIView.as_view(), name='wallet-create'),
    path('wallet-list/', WalletListAPIView.as_view(), name='wallet-list'),
    path('wallet-update/', WalletUpdateAPIView.as_view(), name='wallet-update'),
    path('wallet-delete/', WalletDeleteAPIView.as_view(), name='wallet-delete'),
    path('category-create/', CategoryCreateAPIView.as_view(), name='wallet-create'),
    path('category-list/', CategoryListView.as_view(), name='wallet-list'),
    path('category-update/<int:pk>/', CategoryUpdateView.as_view(), name='wallet-update'),
    path('category-delete/<int:pk>/', CategoryDeleteView.as_view(), name='wallet-delete'),
]