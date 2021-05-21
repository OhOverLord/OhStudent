from django.urls import path

from .views import *

app_name = 'chat'

urlpatterns = [
    path('', ChatListView.as_view()),
    path('create/', ChatCreateView.as_view()),
    path('<int:pk>/', ChatDetailView.as_view()),
    path('<int:pk>/update/', ChatUpdateView.as_view()),
    path('<int:pk>/delete/', ChatDeleteView.as_view()),
    path('friends-list/', FriendsListView.as_view()),
    path('friend-requests-list/', FriendsRequestsView.as_view()),
    path('contact-list/', ContactListView.as_view()),
    path('add-friend/', AddFriendView.as_view()),
    path('delete-friend/', DeleteFriendView.as_view()),
]