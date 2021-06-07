from django.urls import path
from .views import *


app_name = 'finance'
urlpatterns = [
    path('wallet-create/', WalletCreateAPIView.as_view(), name='wallet-create'),
    path('wallet-list/', WalletListAPIView.as_view(), name='wallet-list'),
    path('wallet-update/', WalletUpdateAPIView.as_view(), name='wallet-update'),
    path('wallet-delete/', WalletDeleteAPIView.as_view(), name='wallet-delete'),
    path('wallets-result/', WalletResultAPIView.as_view(), name='wallets-result'),

    path('category-create/', CategoryCreateAPIView.as_view(), name='category-create'),
    path('category-list/', CategoryListView.as_view(), name='category-list'),
    path('category-update/<int:pk>/', CategoryUpdateView.as_view(), name='category-update'),
    path('category-delete/<int:pk>/', CategoryDeleteView.as_view(), name='category-delete'),

    path('consumption-create/', ConsumptionCreateAPIView.as_view(), name='consumption-create'),
    path('consumption-list/', ConsumptionListView.as_view(), name='consumption-list'),
    path('consumption-update/<int:pk>/', ConsumptionUpdateView.as_view(), name='consumption-update'),
    path('consumption-delete/<int:pk>/', ConsumptionDeleteView.as_view(), name='consumption-delete'),
]