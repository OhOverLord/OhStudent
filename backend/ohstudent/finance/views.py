from django.http import Http404
from rest_framework import permissions, serializers
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
from .serializers import ResultSerializer, WalletSerializer, CategorySerializer, ConsumptionSerializer
from django.db.models import Sum


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


class WalletResultAPIView(APIView):
    serializer_class = ResultSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        rubles = Wallet.objects.filter(currency="rubles", user__pk=request.user.pk).aggregate(Sum('money'))
        dollars = Wallet.objects.filter(currency="dollars", user__pk=request.user.pk).aggregate(Sum('money'))
        euros = Wallet.objects.filter(currency="euros", user__pk=request.user.pk).aggregate(Sum('money'))
        data = {}
        data = {
            "rubles": None if rubles["money__sum"] is None else f'{rubles["money__sum"]}₽',
            "dollars": None if dollars["money__sum"] is None else f'{dollars["money__sum"]}$',
            "euros": None if euros["money__sum"] is None else f'{euros["money__sum"]}€',
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


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

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        context = {}
        context.update(serializer.data)
        category = get_object_or_404(Category, spendings__id=serializer.data["id"])
        wallet = get_object_or_404(Wallet, categories__id=category.pk)
        if wallet.money < serializer.validated_data["money"]:
            return Response("Стоимость не может привышать количество денег в кошельке",status=status.HTTP_400_BAD_REQUEST)
        else:
            wallet.money -= serializer.validated_data["money"]
            wallet.save()
            context.update({'balance': wallet.money})
        return Response(context, status=status.HTTP_201_CREATED)


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