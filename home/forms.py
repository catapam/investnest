from django import forms
from .models import Contact
from .signals import FormSignals


class ContactForm(forms.ModelForm):
    """
    A form for users to submit a contact message.
    This form handles saving the data to the Contact model and triggers
    signals based on whether the form submission was successful or not.
    """

    class Meta:
        model = Contact
        # Fields to be displayed in the form
        fields = ['name', 'email', 'message']

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and capture the request object if passed.
        The request object is needed to send the appropriate signal
        with context.
        """
        # Pop 'request' from kwargs
        self.request = kwargs.pop('request', None)
        # Initialize parent class
        super(ContactForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        """
        Override the save method to trigger custom signals for form submission.
        On successful save, it triggers a success signal. If an error occurs,
        an error signal is triggered instead.

        Returns:
            instance (Contact): The saved Contact instance if successful.
        Raises:
            Exception: If there is an error during the save process, the error
            is raised again.
        """
        try:
            # Attempt to save the form data to the Contact model
            instance = super().save(*args, **kwargs)

            # Trigger the success signal if the form was saved correctly
            if self.request:
                FormSignals.form_submission_success.send(
                    # The sender class (ContactForm)
                    sender=self.__class__,
                    # The current request (passed to the signal handler)
                    request=self.request
                )

            return instance  # Return the saved instance

        except Exception as e:
            # In case of an error, trigger the error signal
            if self.request:
                FormSignals.form_submission_error.send(
                    sender=self.__class__,  # The sender class (ContactForm)
                    # The current request (passed to the signal handler)
                    request=self.request
                )

            # Rethrow the exception to propagate the error
            raise e
