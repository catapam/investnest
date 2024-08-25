from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=7, default='#FFFFFF')

    def __str__(self):
        return f'{self.name} (Owned by: {self.user.username})'

    class Meta:
        ordering = ['name']  

class Asset(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='assets')
    name = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_at = models.DateTimeField()

    def __str__(self):
        return f'{self.name} ({self.quantity} units at {self.price} each)'

    class Meta:
        ordering = ['name'] 
