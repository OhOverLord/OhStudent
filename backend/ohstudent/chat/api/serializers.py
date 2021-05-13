from django.db.models import fields
from rest_framework import serializers

from chat.models import Chat, Contact, Message
from chat.views import get_user_contact
from account.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class MessageListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.order_by('-timestamp')
        return super(MessageListSerializer, self).to_representation(data)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        list_serializer_class = MessageListSerializer
        fields = '__all__'


class UserListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.exclude(user=self.context['request'].user)
        return super(UserListSerializer, self).to_representation(data)


class ContactSerializer(serializers.ModelSerializer): 
    user = UserSerializer()

    class Meta:
        model = Contact
        list_serializer_class = UserListSerializer
        fields = ['user',]


class FriendsSerializer(serializers.ModelSerializer):
    friends = ContactSerializer(many=True)
    user = UserSerializer()

    class Meta:
        model = Contact
        fields = '__all__'
        read_only = ('user')


class ChatSerializer(serializers.ModelSerializer):
    participants = ContactSerializer(many=True)
    messages = MessageSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('id', 'messages', 'participants')
        read_only = ('id')

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        chat = Chat()
        chat.save()
        for username in participants:
            contact = get_user_contact(username)
            chat.participants.add(contact)
        chat.save()
        return chat