from django.contrib import messages
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.urls import resolve, reverse
from django.shortcuts import redirect
from django.contrib.auth import REDIRECT_FIELD_NAME


class LoginRequiredMiddleware(MiddlewareMixin):
    """
    Middleware to ensure that users are authenticated before accessing
    specific parts of the application, such as the admin panel
    and operations.

    Handles redirects for login and unauthorized access based
    on user permissions.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Process each view to enforce authentication and authorization rules.
        Redirects users to login or 401 pages when necessary.

        Args:
            request: The current request object.
            view_func: The view function being accessed.
            view_args: Positional arguments for the view.
            view_kwargs: Keyword arguments for the view.

        Returns:
            None or HttpResponse: Returns a redirect or forbidden response
            based on user authentication and authorization status.
        """
        current_url = resolve(request.path_info).url_name

        # Check if the user is not authenticated
        if not request.user.is_authenticated:
            # Allow access to certain URLs without authentication
            allowed_urls = [
                'account_login', 'account_signup', 'account_reset_password',
                'home', 'custom_401', 'custom_404', 'wireframes',
                'account_reset_password_done',
                'account_reset_password_from_key'
                ]
            if current_url not in allowed_urls:
                # Display a warning message and redirect to login page
                messages.warning(request, 'Please log in to access this page.')
                return redirect(
                    f'{reverse("account_login")}?{REDIRECT_FIELD_NAME}='
                    f'{request.get_full_path()}'
                )

        # Enforce superuser access for the admin panel
        elif request.path.startswith(reverse('admin:index')):
            if not request.user.is_authenticated:
                # Redirect unauthenticated users to login
                return redirect(
                    f'{reverse("account_login")}?{REDIRECT_FIELD_NAME}='
                    f'{request.get_full_path()}'
                )
            elif not request.user.is_superuser:
                # Redirect non-superusers to custom 401 page
                return redirect('custom_401')

        # Restrict access to the /operations/ section for staff and superusers
        elif request.path.startswith('/operations/'):
            if not request.user.is_authenticated:
                # Redirect unauthenticated users to login
                messages.warning(request, 'Please log in to access this page.')
                return redirect(
                    f'{reverse("account_login")}?{REDIRECT_FIELD_NAME}='
                    f'{request.get_full_path()}'
                )
            elif not request.user.is_staff:
                # Redirect non-staff users to custom 401 page
                return redirect('custom_401')

        # Allow access if no restrictions are met
        return None
