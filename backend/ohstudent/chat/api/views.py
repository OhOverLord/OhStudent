from typing import List
from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView
)
from rest_framework.views import APIView
from chat.models import Chat, Contact
from account.models import User
from chat.views import get_user_contact
from .serializers import ChatSerializer, FriendsSerializer


class ChatListView(ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        contact = get_user_contact(self.request.user.username)
        queryset = contact.chats.filter(participants__id=self.request.user.id)
        return queryset


class ChatDetailView(APIView):
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, pk):
        try:
            return Chat.objects.get(pk=pk)
        except Chat.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        chat = self.get_object(pk)
        serializer = self.serializer_class(chat, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk, *args, **kwargs):
        chat = self.get_object(pk)
        serializer = self.serializer_class(
            chat, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChatCreateView(CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ChatUpdateView(UpdateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ChatDeleteView(DestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )


class FriendsListView(ListAPIView):
    serializer_class = FriendsSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Contact.objects.all()

    def get_queryset(self):
        contact = get_user_contact(self.request.user.username)
        queryset = contact.friends.all()
        return queryset


class FriendsUpdateView(RetrieveUpdateAPIView):
    serializer_class = FriendsSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, pk):
        try:
            contact = Contact.objects.get(pk=pk)
            return contact
        except:
            contact = Contact()
            contact.user = User.objects.get(pk=pk)
            contact.save()
            return contact

    def update(self, request, *args, **kwargs):
        contact = self.get_object(pk=request.user.pk)
        new_friend = self.get_object(pk=request.data.get('new_friend_id'))
        contact.friends.add(new_friend)
        new_friend.friends.add(contact)
        contact.save()
        new_friend.save()
        friends = contact.friends.all()
        serializer = self.serializer_class(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)