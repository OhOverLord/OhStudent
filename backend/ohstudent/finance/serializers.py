from django.db.models import fields
from rest_framework import serializers

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        read_only = ('user', )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'


class ConsumptionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        read_only = ('date', )