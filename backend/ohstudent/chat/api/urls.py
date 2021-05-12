from django.urls import path

from .views import (
    ChatListView,
    ChatDetailView,
    ChatCreateView,
    ChatUpdateView,
    ChatDeleteView,
    FriendsListView,
    FriendsUpdateView
)

app_name = 'chat'

urlpatterns = [
    path('', ChatListView.as_view()),
    path('create/', ChatCreateView.as_view()),
    path('<int:pk>/', ChatDetailView.as_view()),
    path('<int:pk>/update/', ChatUpdateView.as_view()),
    path('<int:pk>/delete/', ChatDeleteView.as_view()),
    path('friends-list/', FriendsListView.as_view()),
    path('add-friend/', FriendsUpdateView.as_view())
]