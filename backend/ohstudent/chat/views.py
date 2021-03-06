from django.shortcuts import get_object_or_404
from account.models import User
from .models import Chat, Contact


def get_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    messages = chat.messages.order_by('timestamp').all()
    return messages


def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return get_object_or_404(Contact, user=user)


def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)