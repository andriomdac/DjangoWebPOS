from django import forms
from .models import Outflow


class OutflowCreateForm(forms.ModelForm):
    class Meta:
        model = Outflow
        fields = ["quantity",]
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control'})
        }

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity < 1:
            raise forms.ValidationError('Quantidade não pode ser menor ou igual a zero.')
        return quantity
