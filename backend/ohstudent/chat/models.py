from django.db import models
from account.models import User


FRIEND_STATUS = (
    ('добавлен', 'добавлен'),
    ('ожидает', 'ожидает'),
    ('удалён', 'удалён'),
)


class Contact(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    contact = models.ForeignKey(Contact, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact.user.username


class Chat(models.Model):
    participants = models.ManyToManyField(Contact, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return f"{self.pk}"


class Friend(models.Model):
    contact = models.ForeignKey(Contact, blank=True, related_name='friendrequests', on_delete=models.CASCADE)
    friend = models.ForeignKey(Contact, blank=True, related_name='friends', on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=FRIEND_STATUS, null=True, blank=True, default='ожидает')