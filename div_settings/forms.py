from django import forms
from .models import *


# from my side...
class BusinessLocationForm(forms.ModelForm):
    class Meta:
        model = BusinessLocation
        fields = '__all__'


class TaxRateForm(forms.ModelForm):
    class Meta:
        model = TaxRate
        fields = ['name', 'rate']