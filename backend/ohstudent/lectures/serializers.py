from django.db.models import fields
from rest_framework import serializers
from .models import Lecture

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'
        read_only_fields = ('created_at', 'status')