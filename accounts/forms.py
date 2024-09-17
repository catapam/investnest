from django import forms
from django.contrib.auth.models import User

class UpdateUsernameForm(forms.ModelForm):
    """
    Form for updating the username of the currently logged-in user.
    This form is tied to the built-in User model.
    """
    class Meta:
        model = User  # The form is tied to the User model
        fields = ['username']  # Only the 'username' field will be editable

    def __init__(self, *args, **kwargs):
        """
        Custom initialization of the form to add CSS classes for better styling.
        """
        super(UpdateUsernameForm, self).__init__(*args, **kwargs)
        # Add Bootstrap class 'form-control' to the username field
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
