from django import forms
from .models import SaleItem, PaymentMethod, SaleItemReturn
from products.models import Product

class SaleItemForm(forms.ModelForm):
    barcode = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Código de Barras'
        )
    class Meta:
        model = SaleItem
        fields = ["quantity",]
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'quantity': 'Quantidade'
        }



class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ["method_name", "value",]
        widgets = {
            'method_name': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control'})
        }

        labels = {
            'method_name': 'Método de Pagamento',
            'value': 'Valor'
        }


class SaleItemReturnForm(forms.ModelForm):
    class Meta:
        model = SaleItemReturn
        fields = ["quantity", "value",]
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'quantity': 'Quantidade',
            'value': 'Valor',
        }