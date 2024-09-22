from django.dispatch import receiver
from allauth.account.signals import user_logged_in, user_logged_out
from django.contrib import messages

# Signal receiver for user login event
@receiver(user_logged_in)
def on_user_logged_in(request, user, **kwargs):
    """
    This signal is triggered when a user successfully logs in.
    A success message is displayed, welcoming the user by their username.
    
    :param request: The HTTP request object.
    :param user: The user who has logged in.
    :param kwargs: Additional keyword arguments (not used here).
    """
    messages.success(request, f'Welcome back, {user.username}!')

# Signal receiver for user logout event
@receiver(user_logged_out)
def on_user_logged_out(request, **kwargs):
    """
    This signal is triggered when a user logs out.
    A success message is displayed to confirm the logout.
    
    :param request: The HTTP request object.
    :param kwargs: Additional keyword arguments (not used here).
    """
    messages.success(request, 'You have been logged out successfully!')
