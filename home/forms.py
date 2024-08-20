from django import forms
from .models import Contact
from .signals import form_submission_success, form_submission_error

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ContactForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        try:
            # Save the form data
            instance = super().save(*args, **kwargs)
            # Trigger the success signal
            if self.request:
                form_submission_success.send(sender=self.__class__, request=self.request)
            return instance
        except Exception as e:
            # Trigger the error signal
            if self.request:
                form_submission_error.send(sender=self.__class__, request=self.request)
            raise e
