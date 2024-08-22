from django.dispatch import receiver
from django.contrib import messages
from django.db.models.signals import post_save
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def user_profile_updated(sender, instance, created, **kwargs):
    if not created:
        messages.success(instance, 'Your profile has been updated successfully!')