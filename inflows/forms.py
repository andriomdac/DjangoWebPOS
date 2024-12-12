from django import forms
from .models import Inflow

class InflowCreateForm(forms.ModelForm):
    class Meta:
        model = Inflow
        fields = ["quantity",]
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control'})
        }
    
    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity < 0:
            raise forms.ValidationError('Quantidade não pode ser menor que zero.')
        return quantity