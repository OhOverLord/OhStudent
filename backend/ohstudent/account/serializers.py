from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User
from chat.models import Contact


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        contact = Contact()
        contact.user = user
        contact.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255, read_only=True)
    username = serializers.CharField(max_length=255, read_only=True)
    last_name = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'token': user.token,
            'refresh_token': user.refresh_token,
            'username': user.username,
        }


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'token', 'refresh_token')
        read_only_fields = ('token', 'refresh_token',)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance
