from django.db.models import fields
from rest_framework import serializers
from .models import *

class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)

class WalletSerializer(serializers.ModelSerializer):
    currency = ChoiceField(choices=CURRENCIES)
    class Meta:
        model = Wallet
        fields = '__all__'
        read_only = ('user', )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ConsumptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumption
        fields = '__all__'
        read_only = ('date', )


class ResultSerializer(serializers.Serializer):
   rubles = serializers.CharField(allow_null=True, allow_blank=True)
   dollars = serializers.CharField(allow_null=True, allow_blank=True)
   euros = serializers.CharField(allow_null=True, allow_blank=True)