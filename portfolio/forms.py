import random
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from crispy_forms.bootstrap import InlineRadios
from .models import Portfolio, Asset, Transaction
from django.utils import timezone

def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

class PortfolioForm(forms.ModelForm):
    color = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
        label='Portfolio Color'
    )

    class Meta:
        model = Portfolio
        fields = ['name', 'description', 'color']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        user = self.instance.user  # This will now be set correctly in the view

        # Check for duplicate portfolio names for the same user
        if Portfolio.objects.filter(user=user, name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(f'A portfolio with the name "{name}" already exists for this user.')

        return name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.initial.get('color'):
            self.fields['color'].initial = random_color()

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'description',
            Field('color', css_class='colorpicker'),
        )
        self.helper.add_input(Submit('submit', 'Save Portfolio'))

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(AssetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
        )
        self.helper.add_input(Submit('submit', 'Save Asset'))

    def clean_name(self):
        name = self.cleaned_data.get('name')
        portfolio = self.instance.portfolio

        if Asset.objects.filter(portfolio=portfolio, name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(f'An asset with the name "{name}" already exists in this portfolio.')

        return name

class TransactionForm(forms.ModelForm):
    asset_choice = forms.ChoiceField(
        label="Select Asset",
        choices=[],  # We'll populate this in __init__
        required=False,
        help_text="Choose an existing asset or select 'NEW ASSET' to create a new one."
    )
    new_asset_name = forms.CharField(
        required=False,
        label="New Asset Name",
        help_text="Enter the name of the new asset.",
        widget=forms.TextInput(attrs={'style': 'display:block;'}) 
    )
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=timezone.now(),  # Set default to "now"
        required=True
    )

    class Meta:
        model = Transaction
        fields = ['asset_choice', 'new_asset_name', 'action', 'type', 'quantity', 'price', 'date']
        widgets = {
            'action': forms.RadioSelect,  # Render as radio buttons
            'type': forms.RadioSelect,    # Render as radio buttons
        }

    def __init__(self, *args, **kwargs):
        portfolio = kwargs.pop('portfolio', None)
        super(TransactionForm, self).__init__(*args, **kwargs)

        if portfolio:
            asset_choices = [('', '---')]  # Start with the --- option
            asset_choices += [(asset.pk, asset.name) for asset in Asset.objects.filter(portfolio=portfolio).order_by('name')]
            asset_choices.insert(1, ('new', 'NEW ASSET'))  # Add 'NEW ASSET' right after ---
            self.fields['asset_choice'].choices = asset_choices

            initial_asset = kwargs.get('initial', {}).get('asset')
            if initial_asset:
                self.fields['asset_choice'].initial = initial_asset
            else:
                self.fields['asset_choice'].initial = 'new'

        self.fields['action'].choices = Transaction.ACTION_CHOICES
        self.fields['type'].choices = Transaction.TYPE_CHOICES
        self.fields['action'].initial = 'buy'
        self.fields['type'].initial = 'long'

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'asset_choice',
            'new_asset_name',
            InlineRadios('action'),  # Ensure radio buttons are inline
            InlineRadios('type'),    # Ensure radio buttons are inline
            'quantity',
            'price',
            'date',
        )
        self.helper.add_input(Submit('submit', 'Save Transaction'))

    def clean(self):
        cleaned_data = super().clean()
        asset_choice = cleaned_data.get("asset_choice")
        new_asset_name = cleaned_data.get("new_asset_name")

        if asset_choice == 'new' and not new_asset_name:
            raise forms.ValidationError("Please enter a name for the new asset.")

        return cleaned_data

    def save(self, commit=True):
        asset_choice = self.cleaned_data.get("asset_choice")
        new_asset_name = self.cleaned_data.get("new_asset_name")
        portfolio = self.instance.portfolio

        if asset_choice == 'new' and new_asset_name:
            asset, created = Asset.objects.get_or_create(
                name=new_asset_name,
                portfolio=portfolio
            )
        else:
            asset = Asset.objects.get(pk=asset_choice)

        self.instance.asset = asset
        return super(TransactionForm, self).save(commit=commit)
    
    