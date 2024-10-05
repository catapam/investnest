from django import forms
from django.contrib.auth.models import User


class UpdateUsernameForm(forms.ModelForm):
    """
    Form for updating the username of the currently logged-in user.
    This form is tied to the built-in User model.
    """
    class Meta:
        model = User
        fields = ['username']

    def __init__(self, *args, **kwargs):
        super(UpdateUsernameForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})

    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Check if the new username is already taken by another user
        if User.objects.filter(
            username=username
        ).exclude(
            pk=self.instance.pk
        ).exists():
            raise forms.ValidationError(
                "This username is already taken. Please choose another one."
                    )

        return username
