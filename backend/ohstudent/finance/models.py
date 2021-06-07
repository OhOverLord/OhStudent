from django.db import models
from account.models import User


CURRENCIES = (
    ('rubles', '₽'),
    ('dollars', '$'),
    ('euros', '€')
)

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wallets")
    money = models.PositiveIntegerField(default=0)
    description = models.CharField(blank=True, max_length=100)
    currency = models.CharField(max_length=100, choices=CURRENCIES, default='rubles')

    def __str__(self):
        return self.description


class Category(models.Model):
    title = models.CharField(max_length=100)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='categories')


class Consumption(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.CharField(blank=True, max_length=100)
    money = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='spendings')
