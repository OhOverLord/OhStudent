from typing import List
from django.contrib.auth import get_user, get_user_model
from django.db.models import query
from django.http import Http404
from rest_framework import permissions, serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404
)
from rest_framework.views import APIView
from chat.models import Chat, Contact, Friend
from account.models import User
from chat.views import get_user_contact
from .serializers import ChatSerializer, FriendSerializer, ContactSerializer


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


class ChatCreateView(APIView):
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_chat(self, user, interlocutor):
        try:
            chat = Chat.objects.all().filter(participants=user).filter(participants=interlocutor)
            return chat.first()
        except Chat.DoesNotExist:
            chat = Chat.objects.create()
            chat.participants.add(user, interlocutor)
            chat.save()
            return chat

    def post(self, request):
        person_id = request.data.get('person_id')
        user = get_user_contact(request.user.username)
        interlocutor_user = User.objects.get(pk=person_id)
        interlocutor = get_user_contact(interlocutor_user.username)
        chat = self.get_chat(user, interlocutor)
        serializer = self.serializer_class(chat, context={'request': request})
        return Response(serializer.data)



class ChatUpdateView(UpdateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ChatDeleteView(DestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )


class FriendsListView(ListAPIView):
    serializer_class = FriendSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Contact.objects.all()

    def get_queryset(self):
        contact = get_user_contact(self.request.user.username)
        queryset = contact.friends.filter(status='добавлен')
        return queryset


class FriendsRequestsView(ListAPIView):
    serializer_class = FriendSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Contact.objects.all()

    def get_queryset(self):
        contact = get_user_contact(self.request.user.username)
        queryset = contact.friends.all()
        return queryset


class ContactListView(ListAPIView):
    serializer_class = ContactSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        contact = get_user_contact(self.request.user.username)
        friendrequests = contact.friendrequests.all().values('friend')
        friends = contact.friends.all().values('contact')
        return Contact.objects.exclude(id__in=friendrequests).exclude(id__in=friends).exclude(user__pk=self.request.user.id)


class AddFriendView(APIView):
    serializer_class = ContactSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        person_id = request.data.get('person_id')
        contact = get_user_contact(self.request.user.username)
        friend = get_object_or_404(Contact, pk=person_id)
        new_friend = Friend(contact=contact, friend=friend)
        new_friend.save()
        serializer = self.serializer_class(friend)
        return Response(serializer.data)


class DeleteFriendView(APIView):
    serializer_class = ContactSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        person_id = request.data.get('person_id')
        contact = get_user_contact(self.request.user.username)
        friend = Contact.objects.get(user__id=person_id)
        contact.friends.remove(friend)
        serializer = self.serializer_class(friend)
        return Response(serializer.data, status=status.HTTP_200_OK)