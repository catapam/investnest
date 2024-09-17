import re
from django.db import models
from django.core.exceptions import ValidationError

# Base Singleton Model for single-instance models
class SingletonModel(models.Model):
    """
    An abstract model to enforce the singleton pattern.
    Only one instance of a model inheriting this class can exist.
    """
    class Meta:
        abstract = True  # This model won't be created in the database

    def save(self, *args, **kwargs):
        """
        Override save to ensure only one instance of the model exists.
        If an instance already exists, it raises a ValidationError.
        """
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError(
                f'There can be only one {self.__class__.__name__} instance.'
            )
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        """
        Load the single instance of the model or create it if it doesn't exist.
        """
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

# Hero Section Model
class HeroSection(SingletonModel):
    """
    Model to represent the hero section of the homepage, restricted to one instance.
    """
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300)
    background_image = models.ImageField(upload_to='static/images/')
    button_text = models.CharField(max_length=50)
    button_link = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title

# About Section Model
class AboutSection(SingletonModel):
    """
    Model for the about section on the homepage, also restricted to one instance.
    """
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='static/images/', blank=True)
    button_text = models.CharField(max_length=50)
    button_link = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title

# Service Card Model
class ServiceCard(models.Model):
    """
    A model for individual service cards used in the services section.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('in_construction', 'In construction'),
        ('live', 'Live'),
    ]
    
    title = models.CharField(max_length=50)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='draft')
    short_description = models.CharField(max_length=100)
    long_description = models.TextField()

    def __str__(self):
        return self.title

# Services Section Model
class ServicesSection(SingletonModel):
    """
    Model for the services section of the homepage, holding up to 3 service cards.
    """
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=100)
    services = models.ManyToManyField(ServiceCard)

    def clean(self):
        """
        Ensure that no more than 3 service cards are selected.
        """
        if self.services.count() > 3:
            raise ValidationError('You can select a maximum of 3 service cards.')

    def __str__(self):
        return self.title

# Service Order Model
class ServiceOrder(models.Model):
    """
    Model to define the order of services in the services section.
    """
    service_section = models.ForeignKey(ServicesSection, on_delete=models.CASCADE)
    service = models.ForeignKey(ServiceCard, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']  # Default ordering is by 'order'

# Pricing Plan Model
class PricingPlan(models.Model):
    """
    Model for individual pricing plans displayed in the pricing section.
    """
    title = models.CharField(max_length=15)
    price_description = models.CharField(max_length=15)
    features = models.TextField()
    button_text = models.CharField(max_length=50)
    button_link = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title

    def get_features_list(self):
        """
        Split features by commas or newlines into a list for display purposes.
        """
        return [feature.strip() for feature in re.split(r'[,\n]', self.features) if feature.strip()]

# Pricing Section Model
class PricingSection(SingletonModel):
    """
    Model for the pricing section of the homepage, holding up to 3 pricing plans.
    """
    title = models.CharField(max_length=200)
    plans = models.ManyToManyField(PricingPlan)

    def clean(self):
        """
        Ensure that no more than 3 pricing plans are selected.
        """
        if self.plans.count() > 3:
            raise ValidationError('You can select a maximum of 3 pricing plans.')

    def __str__(self):
        return self.title

# Pricing Order Model
class PricingOrder(models.Model):
    """
    Model to define the order of pricing plans in the pricing section.
    """
    pricing_section = models.ForeignKey(PricingSection, on_delete=models.CASCADE)
    pricing = models.ForeignKey(PricingPlan, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']  # Default ordering is by 'order'

# Contact Model
class Contact(models.Model):
    """
    Model to represent a contact message submitted by a user.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
