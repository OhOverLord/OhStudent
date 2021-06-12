from django.db import models
from django.db.models.base import Model
from rest_framework import status
from account.models import User

STATUS = (
    ('completed', 'completed'),
    ('process', 'process'),
)


class Date(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='days', null=True)
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()


class Task(models.Model):
    title = models.CharField(max_length=150)
    time_from = models.CharField(max_length=6)
    time_to = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=150, choices=STATUS, default='process')
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    