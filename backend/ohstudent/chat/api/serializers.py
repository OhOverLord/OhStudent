from django.db.models import fields
from rest_framework import serializers

from chat.models import Chat, Contact, Message, Friend
from chat.views import get_user_contact
from account.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class MessageListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.order_by('-timestamp')
        return super(MessageListSerializer, self).to_representation(data)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        list_serializer_class = MessageListSerializer
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer): 
    user = UserSerializer()

    class Meta:
        model = Contact
        fields = ['user',]


class FriendSerializer(serializers.ModelSerializer):
    friend = ContactSerializer()
    contact = ContactSerializer()
    
    class Meta:
        model = Friend
        fields = ('friend', 'contact', 'status')
        read_only = ('friend', 'contact')


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