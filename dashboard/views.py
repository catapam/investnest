from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView


# Class-based view for the dashboard page, requires login
@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'


# Class-based view to handle the redirection to the main dashboard page
@method_decorator(login_required, name='dispatch')
class RedirectDashboardView(RedirectView):
    """
    Class-based view to redirect the user to the update dashboard page.
    Ensures that only logged-in users can access this redirect.
    """
    pattern_name = 'dashboard'  # Redirects to the URL pattern

    def get_redirect_url(self, *args, **kwargs):
        """
        Return the URL to redirect to.
        """
        return super().get_redirect_url(*args, **kwargs)
