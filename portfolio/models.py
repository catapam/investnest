from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=14)
    description = models.TextField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=7, default='#FFFFFF')

    def __str__(self):
        return f'{self.name} (Owned by: {self.user.username})'

    class Meta:
        ordering = ['name']

class Asset(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='assets')
    name = models.CharField(max_length=255)
    live_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_total_quantity(self):
        transactions = self.transactions.all()
        total_quantity = sum(
            transaction.quantity if transaction.action == 'buy' else -transaction.quantity
            for transaction in transactions
        )
        return total_quantity

    def get_total_value(self):
        total_quantity = self.get_total_quantity()
        return total_quantity * self.live_price if self.live_price else 0

    class Meta:
        ordering = ['name']

class Transaction(models.Model):
    ACTION_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]

    TYPE_CHOICES = [
        ('long', 'Long'),
        ('short', 'Short'),
    ]
    
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='transactions')
    action = models.CharField(max_length=4, choices=ACTION_CHOICES)
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)  # Set default to "now", but allow editing

    def __str__(self):
        return f'{self.get_action_display()} {self.quantity} {self.asset.name} at {self.price}'

    class Meta:
        ordering = ['-date']