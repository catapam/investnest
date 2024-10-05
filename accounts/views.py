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
    Requires the user to be logged in and provides success or error messages
    based on the form submission.
    """

    # Define the template that will be used to render the form
    template_name = 'accounts/update_username.html'

    # Use the UpdateUsernameForm to handle the form logic
    form_class = UpdateUsernameForm

    # Redirect the user to the dashboard after successful form submission
    success_url = reverse_lazy('dashboard')

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests (form submissions).
        Checks if the form is valid. If valid, calls form_valid(),
        otherwise form_invalid().
        """
        form = self.get_form()  # Get the form instance
        if form.is_valid():
            # If the form is valid, process it
            return self.form_valid(form)
        else:
            # If the form is invalid, handle the errors
            return self.form_invalid(form)

    def get_form(self, form_class=None):
        """
        Override the get_form method to bind the form to the current user
        instance.

        This ensures that the form updates the logged-in user's username.
        """
        if self.request.method == 'POST':
            # Bind the form to POST data and the current user instance
            return self.form_class(
                self.request.POST,
                instance=self.request.user
                    )
        # Bind the form only to the current user instance for GET requests
        return self.form_class(instance=self.request.user)

    def form_valid(self, form):
        """
        Handle valid form submissions.
        Save the form and display a success message.
        """
        form.save()  # Save the updated username
        # Add a success message to display to the user after updating username
        messages.success(
            self.request,
            'Your username has been updated successfully!'
                )
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Handle invalid form submissions.
        Display an error message and re-render the form.
        """
        # Add an error message to inform the user about the submission failure
        messages.error(
            self.request,
            'There was an error updating your username. Please try again.'
                )
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
