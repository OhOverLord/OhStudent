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


class CategoryCreateAPIView(CreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryUpdateView(UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated, )


class CategoryDeleteView(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated, )


class CategoryListView(APIView):
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        wallet_pk = request.data.pop('wallet', None)
        if wallet_pk is not None:
            wallet = get_object_or_404(Wallet, pk=wallet_pk)
            categories = Category.objects.filter(wallet=wallet)
            serializer = self.serializer_class(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class ConsumptionCreateAPIView(CreateAPIView):
    serializer_class = ConsumptionSerializer
    queryset = Consumption.objects.all()


class ConsumptionUpdateView(UpdateAPIView):
    queryset = Consumption.objects.all()
    serializer_class = ConsumptionSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ConsumptionDeleteView(DestroyAPIView):
    queryset = Consumption.objects.all()
    serializer_class = ConsumptionSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ConsumptionListView(APIView):
    serializer_class = ConsumptionSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        category_pk = request.data.pop('category', None)
        if category_pk is not None:
            category = get_object_or_404(Category, pk=category_pk)
            consumptions = Consumption.objects.filter(category=category)
            serializer = self.serializer_class(consumptions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)