from django.db import models
from django.contrib.auth.models import User


class Sector(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Stock(models.Model):
    symbol = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, related_name='stocks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    exposed_to_sectors = models.ManyToManyField(Sector, related_name='exposed_to_sectors')

    current_price = models.FloatField(null=True, blank=True)
    SMA_50 = models.FloatField(null=True, blank=True)
    SMA_200 = models.FloatField(null=True, blank=True)
    RSI_14 = models.FloatField(null=True, blank=True)

    WMA_30_week = models.FloatField(null=True, blank=True)
    SMA_50_week = models.FloatField(null=True, blank=True)
    SMA_200_week = models.FloatField(null=True, blank=True)

    RS_SP500 = models.FloatField(null=True, blank=True)

    new_high = models.BooleanField(default=False)
    new_low = models.BooleanField(default=False)
    volume_spike = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.symbol} - {self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    stocks = models.ManyToManyField(Stock, related_name='tags')

    def __str__(self):
        return self.name


class StockList(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stock_lists')
    stocks = models.ManyToManyField(Stock, related_name='in_lists')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return f"{self.user.username}'s {self.name}"