from django.dispatch import receiver
from allauth.account.signals import user_logged_in, user_logged_out
from django.contrib import messages

@receiver(user_logged_in)
def on_user_logged_in(request, user, **kwargs):
    messages.success(request, f'Welcome back, {user.username}!')

@receiver(user_logged_out)
def on_user_logged_out(request, **kwargs):
    messages.success(request, 'You have been logged out successfully!')
