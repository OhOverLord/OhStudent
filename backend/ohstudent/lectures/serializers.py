from django.db.models import fields
from rest_framework import serializers
from .models import Lecture

class LectureSerializer(serializers.ModelSerializer):
    absolute_url = serializers.URLField(source='get_absolute_url', read_only=True) 
    
    class Meta:
        model = Lecture
        fields = ['title', 'description', 'created_at', 'status', 'updated_at', 'absolute_url']
        read_only_fields = ('created_at', 'status', 'absolute_url', 'updated_at')