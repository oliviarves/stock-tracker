from django.db import models
from django.contrib.auth.models import User
from stocks.models import Stock, Sector


class StockImage(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='images')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='stock_images')
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='stock_images/')
    description = models.TextField(blank=True, null=True)
    timeframe = models.CharField(max_length=50, blank=True, null=True)
    analysis_type = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.stock.symbol} - {self.title or 'Unnamed'}"


class StockNote(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='notes')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='stock_notes')
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.stock.symbol} - {self.title or 'Unnamed'}"


class StockEvaluation(models.Model):

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='evaluations')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='stock_evaluations')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 rating
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('stock', 'user', 'evaluation_type')

    def __str__(self):
        return f"{self.stock.symbol} - ({self.rating})"


class SectorImage(models.Model):
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='images')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sector_images')
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='sector_images/')
    description = models.TextField(blank=True, null=True)
    analysis_type = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sector.name} - {self.title or 'Unnamed'}"


class SectorNote(models.Model):
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='notes')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sector_notes')
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sector.name} - {self.title or 'Unnamed'}"


class SectorEvaluation(models.Model):

    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='evaluations')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sector_evaluations')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 rating
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.sector.name} - ({self.rating})"