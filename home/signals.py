from django.dispatch import Signal, receiver
from django.contrib import messages

# Define custom signals
form_submission_success = Signal()
form_submission_error = Signal()

# Signal handlers
@receiver(form_submission_success)
def on_form_submission_success(request, **kwargs):
    messages.success(request, 'Your message has been sent successfully!')

@receiver(form_submission_error)
def on_form_submission_error(request, **kwargs):
    messages.error(request, 'An error occurred while submitting the form. Please contact by email: support@investnest.com')
