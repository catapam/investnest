from django.dispatch import Signal, receiver
from django.contrib import messages


# Define custom signals
class FormSignals:
    """Class to define and handle form-related signals."""

    # Custom signals for form submission
    form_submission_success = Signal()
    form_submission_error = Signal()

    @staticmethod
    @receiver(form_submission_success)
    def handle_form_submission_success(request, **kwargs):
        """Handles successful form submission by showing a success message."""
        messages.success(request, 'Your message has been sent successfully!')

    @staticmethod
    @receiver(form_submission_error)
    def handle_form_submission_error(request, **kwargs):
        """Handles form submission errors by showing an error message."""
        messages.error(
            request, 'An error occurred while submitting the form. '
            'Please contact support via email: support@investnest.com.'
        )


# Instantiate the FormSignals class to ensure handlers are connected
form_signals = FormSignals()
