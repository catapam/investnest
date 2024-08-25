import random
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from .models import Portfolio, Asset

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
    purchased_at = forms.DateTimeField(
        widget=forms.TextInput(attrs={'class': 'form-control datepicker', 'data-provide': 'datepicker'})
    )

    class Meta:
        model = Asset
        fields = ['name', 'quantity', 'price', 'purchased_at']

    def __init__(self, *args, **kwargs):
        super(AssetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'quantity',
            'price',
            Field('purchased_at', css_class='datepicker')
        )
        self.helper.add_input(Submit('submit', 'Save Asset'))
