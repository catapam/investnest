import random
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from crispy_forms.bootstrap import InlineRadios
from .models import Portfolio, Asset, Transaction
from django.utils import timezone

def random_color():
    """
    Generate a random hexadecimal color code.
    
    Returns:
        str: Random hexadecimal color code in the format #RRGGBB.
    """
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

class PortfolioForm(forms.ModelForm):
    """
    Form for creating and updating a Portfolio model instance.
    """
    color = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
        label='Portfolio Color'
    )

    class Meta:
        model = Portfolio
        fields = ['name', 'description', 'color']

    def clean_name(self):
        """
        Validate the portfolio name to ensure uniqueness for the current user.
        """
        name = self.cleaned_data.get('name')
        user = self.instance.user

        # Check for duplicate portfolio names for the same user
        if Portfolio.objects.filter(user=user, name=name).exclude(
                pk=self.instance.pk).exists():
            raise forms.ValidationError(
                f'A portfolio with the name "{name}" already exists for this user.')

        return name

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and set the color field to a random color if not provided.
        """
        super().__init__(*args, **kwargs)
        if not self.initial.get('color'):
            self.fields['color'].initial = random_color()

        # Initialize the form layout using crispy-forms
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'description',
            Field('color', css_class='colorpicker'),
        )
        self.helper.add_input(Submit('submit', 'Save Portfolio'))

class AssetForm(forms.ModelForm):
    """
    Form for creating and updating an Asset model instance.
    """
    class Meta:
        model = Asset
        fields = ['name']

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and set up the layout using crispy-forms.
        """
        super(AssetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout('name')
        self.helper.add_input(Submit('submit', 'Save Asset'))

    def clean_name(self):
        """
        Validate the asset name to ensure uniqueness within the portfolio.
        """
        name = self.cleaned_data.get('name')
        portfolio = self.instance.portfolio

        if Asset.objects.filter(portfolio=portfolio, name=name).exclude(
                pk=self.instance.pk).exists():
            raise forms.ValidationError(
                f'An asset with the name "{name}" already exists in this portfolio.')

        return name

class TransactionForm(forms.ModelForm):
    """
    Form for creating and updating a Transaction model instance.
    Provides options to either choose an existing asset or create a new one.
    """
    asset_choice = forms.ChoiceField(
        label="Select Asset",
        choices=[],  # Will be populated in __init__
        required=False,
        help_text="Choose an existing asset or select 'NEW ASSET' to create a new one."
    )
    new_asset_name = forms.CharField(
        required=False,
        label="New Asset Name",
        max_length=8,  # Enforce max length
        help_text="Enter the name of the new asset (Max length: 8 characters).",
        widget=forms.TextInput(attrs={'style': 'display:block;'})
    )
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=timezone.now(),
        required=True
    )

    class Meta:
        model = Transaction
        fields = ['asset_choice', 'new_asset_name', 'action', 'type', 'quantity', 'price', 'date']
        widgets = {
            'action': forms.RadioSelect,
            'type': forms.RadioSelect,
        }

    def clean_new_asset_name(self):
        new_asset_name = self.cleaned_data.get('new_asset_name')
        if new_asset_name and len(new_asset_name) > 8:
            raise forms.ValidationError("Asset name cannot exceed 8 characters.")
        return new_asset_name

    def clean_date(self):
        date = self.cleaned_data['date']
        if timezone.is_naive(date):
            # Make the datetime timezone-aware
            date = timezone.make_aware(date)
        return date

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with portfolio-specific assets.
        Set the initial asset choice and default values for action and type fields.
        """
        portfolio = kwargs.pop('portfolio', None)
        super(TransactionForm, self).__init__(*args, **kwargs)

        if portfolio:
            asset_choices = [('', '---')]  # Default empty choice
            asset_choices += [(asset.pk, asset.name) for asset in Asset.objects.filter(
                portfolio=portfolio).order_by('name')]
            asset_choices.insert(1, ('new', 'NEW ASSET'))  # Add 'NEW ASSET' option
            self.fields['asset_choice'].choices = asset_choices

        self.fields['action'].choices = Transaction.ACTION_CHOICES
        self.fields['type'].choices = Transaction.TYPE_CHOICES
        self.fields['action'].initial = 'buy'
        self.fields['type'].initial = 'long'

        # Initialize the form layout using crispy-forms
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'asset_choice',
            'new_asset_name',
            InlineRadios('action'),
            InlineRadios('type'),
            'quantity',
            'price',
            'date',
        )
        self.helper.add_input(Submit('submit', 'Save Transaction'))

    def clean(self):
        """
        Validate the form to ensure the new asset name is provided if 'NEW ASSET' is selected.
        """
        cleaned_data = super().clean()
        asset_choice = cleaned_data.get("asset_choice")
        new_asset_name = cleaned_data.get("new_asset_name")

        if asset_choice == 'new' and not new_asset_name:
            raise forms.ValidationError("Please enter a name for the new asset.")

        return cleaned_data
