from django.db.models import fields
from rest_framework import serializers
from .models import Lecture, Folder
from account.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class LectureSerializer(serializers.ModelSerializer):
    absolute_url = serializers.URLField(source='get_absolute_url', read_only=True)
    
    class Meta:
        model = Lecture
        fields = '__all__'
        read_only_fields = ('created_at', 'status', 'absolute_url', 'updated_at')


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'


class LectureDetailSerializer(serializers.ModelSerializer):
    absolute_url = serializers.URLField(source='get_absolute_url', read_only=True)
    user = UserSerializer()
    
    class Meta:
        model = Lecture
        fields = '__all__'
        read_only_fields = ('created_at', 'status', 'absolute_url', 'updated_at')