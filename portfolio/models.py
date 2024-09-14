from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=12)
    description = models.TextField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=7, default='#FFFFFF')
    total_value = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    total_num_assets = models.PositiveIntegerField(default=0)
    total_num_transactions = models.PositiveIntegerField(default=0)

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

    def update_portfolio_stats(self):
        self.total_value = sum(asset.total_value for asset in self.assets.all())
        self.total_num_assets = self.assets.count()
        self.total_num_transactions = Transaction.objects.filter(asset__portfolio=self).count()
        self.save()

    def save(self, *args, **kwargs):
        self.clean()  
        super().save(*args, **kwargs)

class Asset(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='assets')
    name = models.CharField(max_length=6)
    
    # New fields to store values
    total_quantity = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    average_price = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    total_value = models.DecimalField(max_digits=20, decimal_places=8, default=0)

    def __str__(self):
        return self.name

    # Returning stored values
    def get_total_quantity(self):
        return self.total_quantity

    def get_average_price(self):
        return self.average_price

    def get_total_value(self):
        return self.total_value

    # Clean method for asset uniqueness validation
    def clean(self):
        if Asset.objects.filter(portfolio=self.portfolio, name=self.name).exclude(pk=self.pk).exists():
            raise ValidationError(f'An asset with the name "{self.name}" already exists in this portfolio.')

    # Overriding the save method to ensure validation before saving
    def save(self, *args, **kwargs):
        self.clean() 
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['portfolio', 'name'], name='unique_asset_per_portfolio')
        ]

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
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    price = models.DecimalField(max_digits=16, decimal_places=4)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.get_action_display()} {self.quantity} {self.asset.name} at {self.price}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_asset_values()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.update_asset_values()

    def update_asset_values(self):
        # Get all transactions related to the asset
        transactions = self.asset.transactions.all()
        
        # Update total quantity, total value, and average price
        total_quantity = sum(
            transaction.quantity if (transaction.action == 'buy' and transaction.type == 'long') or 
                                    (transaction.action == 'sell' and transaction.type == 'short')
            else -transaction.quantity
            for transaction in transactions
        )

        total_value = sum(
            transaction.quantity * transaction.price if (transaction.action == 'buy' and transaction.type == 'long') or 
                                                        (transaction.action == 'sell' and transaction.type == 'short')
            else -(transaction.quantity * transaction.price)
            for transaction in transactions
        )

        average_price = total_value / total_quantity if total_quantity != 0 else 0

        # Update the asset's stored values
        self.asset.total_quantity = total_quantity
        self.asset.total_value = total_value
        self.asset.average_price = average_price
        self.asset.save()

    class Meta:
        ordering = ['-date']
