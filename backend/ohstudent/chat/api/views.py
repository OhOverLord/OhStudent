from django.http import Http404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    DestroyAPIView,
    UpdateAPIView,
    CreateAPIView,
    get_object_or_404
)
from rest_framework.views import APIView
from chat.models import Chat, Contact, Friend
from account.models import User
from chat.views import get_user_contact
from .serializers import ChatSerializer, FriendSerializer, ContactSerializer, GetChatSerializer
from django.db.models import Q


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

    def get_object(self, pk, user):
        try:
            return Chat.objects.get(pk=pk, participants=user)
        except Chat.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = get_user_contact(request.user.username)
        chat = self.get_object(pk, user)
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
    queryset = Chat.objects.all()
    serializer_class = GetChatSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        request_data = request.data
        participants = request_data['participants']
        participants_contacts = []
        for username in participants:
            contact = get_user_contact(username)
            participants_contacts.append(contact.id)
        request_data['participants'] = participants_contacts
        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
        return Friend.objects.filter(Q(contact=contact) | Q(friend=contact)).filter(status="добавлен")


class FriendsRequestsView(ListAPIView):
    serializer_class = FriendSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Contact.objects.all()

    def get_queryset(self):
        contact = get_user_contact(self.request.user.username)
        return Friend.objects.filter(friend=contact).filter(status="ожидает")


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


class ApplyFriendView(APIView):
    serializer_class = ContactSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        person_id = request.data.get('person_id')
        contact = get_user_contact(self.request.user.username)
        friend_request = get_object_or_404(Contact, pk=person_id)
        friends = Friend.objects.get(contact=friend_request, friend=contact)
        friends.status = "добавлен"
        friends.save()
        serializer = self.serializer_class(friend_request)
        return Response(serializer.data)


class DeleteFriendView(APIView):
    serializer_class = ContactSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        person_id = request.data.get('person_id')
        contact = get_user_contact(self.request.user.username)
        friend = get_object_or_404(Contact, pk=person_id)
        friends = Friend.objects.filter(Q(contact=contact, friend=friend) | Q(contact=friend, friend=contact))
        friends.delete()
        serializer = self.serializer_class(friend)
        return Response(serializer.data, status=status.HTTP_200_OK)