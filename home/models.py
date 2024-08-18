import re
from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError(f'There can be only one {self.__class__.__name__} instance.')
        super(SingletonModel, self).save(*args, **kwargs)
        
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    
class HeroSection(SingletonModel):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300)
    background_image = models.ImageField(upload_to='static/images/')
    button_text = models.CharField(max_length=50)
    button_link = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.title

class AboutSection(SingletonModel):
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='static/images/', blank=True)
    button_text = models.CharField(max_length=50)
    button_link = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.title

class ServiceCard(models.Model):
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

class ServicesSection(SingletonModel):
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=100)
    services = models.ManyToManyField(ServiceCard)

    def clean(self):
        if self.services.count() > 3:
            raise ValidationError('You can select a maximum of 3 pricing plans.')

    def __str__(self):
        return self.title

class ServiceOrder(models.Model):
    service_section = models.ForeignKey(ServicesSection, on_delete=models.CASCADE)
    service = models.ForeignKey(ServiceCard, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

class PricingPlan(models.Model):
    title = models.CharField(max_length=15)
    price_description = models.CharField(max_length=15)
    features = models.TextField()
    button_text = models.CharField(max_length=50)
    button_link = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title

    def get_features_list(self):
        # Split the features by either commas or newlines and strip any extra whitespace
        return [feature.strip() for feature in re.split(r'[,\n]', self.features) if feature.strip()]

class PricingSection(SingletonModel):
    title = models.CharField(max_length=200)
    plans = models.ManyToManyField(PricingPlan)

    def clean(self):
        if self.plans.count() > 3:
            raise ValidationError('You can select a maximum of 3 pricing plans.')
    
    def __str__(self):
        return self.title

class PricingOrder(models.Model):
    pricing_section = models.ForeignKey(PricingSection, on_delete=models.CASCADE)
    pricing = models.ForeignKey(PricingPlan, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
