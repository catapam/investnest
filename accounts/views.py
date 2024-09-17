from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView
from .forms import UpdateUsernameForm
from django.shortcuts import redirect


@method_decorator(login_required, name='dispatch')
class UpdateUsernameView(FormView):
    """
    View for updating the username of the currently logged-in user.
    This form requires the user to be logged in and will display success or error messages based on form submission.
    """
    template_name = 'accounts/update_username.html'  # Template for the update form
    form_class = UpdateUsernameForm  # Form class to handle username update
    success_url = reverse_lazy('dashboard')  # Redirect to the dashboard on success

    def get_form(self, form_class=None):
        """
        Override the get_form method to provide the form with the current user instance.
        """
        return self.form_class(instance=self.request.user)

    def form_valid(self, form):
        """
        Handle valid form submissions. Save the form and display a success message.
        """
        form.save()
        messages.success(self.request, 'Your username has been updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Handle invalid form submissions. Display an error message.
        """
        messages.error(self.request, 'There was an error updating your username. Please try again.')
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
class RedirectUserView(RedirectView):
    """
    Class-based view to redirect the user to the update username page.
    Ensures that only logged-in users can access this redirect.
    """
    pattern_name = 'account_user'  # Redirects to the URL pattern

    def get_redirect_url(self, *args, **kwargs):
        """
        Return the URL to redirect to.
        """
        return super().get_redirect_url(*args, **kwargs)
