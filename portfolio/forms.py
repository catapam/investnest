import random
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from .models import Portfolio, Asset, Transaction

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        widget=forms.TextInput(attrs={'style': 'display:none;'})  # Initially hidden
    )

    class Meta:
        model = Transaction
        fields = ['asset_choice', 'new_asset_name', 'action', 'type', 'quantity', 'price']

    def __init__(self, *args, **kwargs):
        portfolio = kwargs.pop('portfolio', None)
        super(TransactionForm, self).__init__(*args, **kwargs)

        if portfolio:
            # Get existing assets and sort them alphabetically by name
            asset_choices = [(asset.pk, asset.name) for asset in Asset.objects.filter(portfolio=portfolio).order_by('name')]

            # Add 'NEW ASSET' at the top and "---" as the default option
            asset_choices.insert(0, ('new', 'NEW ASSET'))
            asset_choices.insert(0, ('', '---'))

            self.fields['asset_choice'].choices = asset_choices

            # Handle the initial value for the dropdown
            initial_asset = kwargs.get('initial', {}).get('asset')
            if initial_asset:
                # Set the initial asset selection if provided
                self.fields['asset_choice'].initial = initial_asset
            else:
                # Default to "---" if no initial asset is provided
                self.fields['asset_choice'].initial = ''

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'asset_choice',
            'new_asset_name',
            'action',
            'type',
            'quantity',
            'price',
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
            # Ensure portfolio is set correctly when creating a new asset
            asset, created = Asset.objects.get_or_create(
                name=new_asset_name,
                portfolio=portfolio
            )
        else:
            asset = Asset.objects.get(pk=asset_choice)

        self.instance.asset = asset
        return super(TransactionForm, self).save(commit=commit)
