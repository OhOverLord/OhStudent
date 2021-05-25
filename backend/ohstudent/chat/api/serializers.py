from django.db.models import fields
from rest_framework import serializers

from chat.models import Chat, Contact, Message, Friend
from chat.views import get_user_contact
from rest_framework.generics import get_object_or_404
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


class GetContactSerializer(serializers.StringRelatedField):        
    def to_internal_value(self, value):
        return value


class GetChatSerializer(serializers.ModelSerializer):
    participants = GetContactSerializer(many=True)
    messages = MessageSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('id', 'messages', 'participants')
        read_only = ('id')

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        chat = Chat.objects.filter(participants=participants[0]).filter(participants=participants[1])
        if chat.exists():
            return chat.first()
        else:
            new_chat = Chat()
            new_chat.save()
            for user_id in participants:
                contact = get_object_or_404(Contact, pk=user_id)
                new_chat.participants.add(contact)
            new_chat.save()
            return new_chat


class ParticipantListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(participants__user=self.context['request'].user)
        return super(ParticipantListSerializer, self).to_representation(data)


class ChatSerializer(serializers.ModelSerializer):
    participants = ContactSerializer(many=True)
    messages = MessageSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('id', 'messages', 'participants')
        list_serializer_class = ParticipantListSerializer
        read_only = ('id')
            