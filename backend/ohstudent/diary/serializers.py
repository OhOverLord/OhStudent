from django.db.models import fields
from rest_framework import serializers
from .models import *


class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only = ('created_at', )


class TaskDetailSerializer(serializers.ModelSerializer):
    date = DateSerializer()
    class Meta:
        model = Task
        fields = '__all__'
        read_only = ('created_at', )