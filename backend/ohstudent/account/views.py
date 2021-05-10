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
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.pk)
        serializer = self.serializer_class(user)
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
            raise jwt.exceptions.InvalidTokenError(
                'expired refresh token, please login again.')

        user = User.objects.filter(id=payload.get('id')).first()
        if user is None:
            raise jwt.exceptions.InvalidKeyError('User not found')

        if not user.is_active:
            raise jwt.exceptions.InvalidKeyError('user is inactive')

        token = user.token
        return Response({'token': token, 'refresh_token': user.refresh_token})


class ComparePassword(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        password = request.data.get('password')
        user = User.objects.get(pk=request.user.pk)
        if user.check_password(password):
            print("success")
            return Response("Success", status=status.HTTP_200_OK)
        else:
            print("wrong")
            return Response({"errors": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST)
