import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer
from .renderers import UserJSONRenderer
from .models import User


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        print(user)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class RefreshTokenAPIView(APIView):
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer, )
    

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if refresh_token is None:
            raise jwt.exceptions.AuthenticationFailed(
                'Authentication credentials were not provided.')
        try:
            payload = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise jwt.exceptions.AuthenticationFailed(
                'expired refresh token, please login again.')

        user = User.objects.filter(id=payload.get('id')).first()
        if user is None:
            raise jwt.exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise jwt.exceptions.AuthenticationFailed('user is inactive')

        token = user.token
        return Response({'token': token, 'refresh_token': user.refresh_token})
