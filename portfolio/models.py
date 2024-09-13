from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=14)
    description = models.TextField(max_length=150, blank=True, null=True)
    color = models.CharField(max_length=7, default='#FFFFFF')

    def __str__(self):
        return f'{self.name} (Owned by: {self.user.username})'

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_portfolio_per_user')
        ]
        
    def clean(self):
        if Portfolio.objects.filter(user=self.user, name=self.name).exclude(pk=self.pk).exists():
            raise ValidationError(f'A portfolio with the name "{self.name}" already exists for this user.')

    def save(self, *args, **kwargs):
        self.clean()  
        super().save(*args, **kwargs)

class Asset(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='assets')
    name = models.CharField(max_length=6)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_total_quantity(self):
        transactions = self.transactions.all()
        total_quantity = sum(
            transaction.quantity if (transaction.action == 'buy' and transaction.type == 'long') or
                                    (transaction.action == 'sell' and transaction.type == 'short')
            else -transaction.quantity
            for transaction in transactions
        )
        return total_quantity

    def get_average_price(self):
        transactions = self.transactions.all()
        weighted_sum = 0
        total_quantity = 0
        
        for transaction in transactions:
            quantity = transaction.quantity if (transaction.action == 'buy' and transaction.type == 'long') or \
                                            (transaction.action == 'sell' and transaction.type == 'short') \
                                        else -transaction.quantity
            weighted_sum += quantity * transaction.price
            total_quantity += quantity
        
        if total_quantity == 0:
            return 0
    
        return round(weighted_sum / total_quantity, 4)

    def get_total_value(self):
        total_quantity = self.get_total_quantity()
        average_price = self.get_average_price()
        return round(total_quantity * average_price, 4) if average_price else 0

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['portfolio', 'name'], name='unique_asset_per_portfolio')
        ]

    def clean(self):
        if Asset.objects.filter(portfolio=self.portfolio, name=self.name).exclude(pk=self.pk).exists():
            raise ValidationError(f'An asset with the name "{self.name}" already exists in this portfolio.')

    def save(self, *args, **kwargs):
        self.clean() 
        super().save(*args, **kwargs)

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