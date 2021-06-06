from django.http import Http404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    DestroyAPIView,
    UpdateAPIView,
    CreateAPIView,
    get_object_or_404
)
from rest_framework.views import APIView
from .models import Wallet, Category, Consumption
from .serializers import WalletSerializer, CategorySerializer, ConsumptionSerializer


class WalletCreateAPIView(APIView):
    serializer_class = WalletSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        request_data = request.data
        request_data['user'] = request.user.pk
        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WalletListAPIView(ListAPIView):
    serializer_class = WalletSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Wallet.objects.filter(user__pk=self.request.user.pk)


class WalletUpdateAPIView(APIView):
    serializer_class = WalletSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        pk = request.data.pop('id', None)
        if pk is not None:
            wallet = get_object_or_404(Wallet, pk=pk, user__id=request.user.pk)
            serializer = self.serializer_class(
                wallet, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class WalletDeleteAPIView(APIView):
    serializer_class = WalletSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        pk = request.data.pop('id', None)
        wallet = get_object_or_404(Wallet, pk=pk, user__id=request.user.pk)
        wallet.delete()
        return Response(status=status.HTTP_200_OK)
