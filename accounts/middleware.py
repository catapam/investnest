from django.contrib import messages
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.urls import resolve, reverse
from django.shortcuts import redirect, render
from django.http import HttpResponseForbidden
from django.contrib.auth import REDIRECT_FIELD_NAME

class LoginRequiredMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Ensure the user is logged in for all pages except login, signup, and reset password
        if not request.user.is_authenticated:
            current_url = resolve(request.path_info).url_name
            if current_url not in ['account_login', 'account_signup', 'account_reset_password', 'home', 'custom_401', 'custom_404']:
                messages.warning(request, 'Please log in to access this page.')
                return redirect(f'{reverse("account_login")}?{REDIRECT_FIELD_NAME}={request.get_full_path()}')

        # Ensure only superusers can access the admin panel
        elif request.path.startswith(reverse('admin:index')):
            if not request.user.is_authenticated:
                return redirect(f'{reverse("account_login")}?{REDIRECT_FIELD_NAME}={request.get_full_path()}')
            elif not request.user.is_superuser:
                return redirect('custom_401')

        # Restrict access to the /operations/ section to staff and superusers only
        elif request.path.startswith('/operations/'):
            if not request.user.is_authenticated:
                messages.warning(request, 'Please log in to access this page.')
                return redirect(f'{reverse("account_login")}?{REDIRECT_FIELD_NAME}={request.get_full_path()}')
            elif not request.user.is_staff:
                return redirect('custom_401')

        return None
