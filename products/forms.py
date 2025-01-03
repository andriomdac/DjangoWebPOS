from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["created_at", "updated_at", "quantity",]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autofocus': ''}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01}),
            'barcode': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),

        }

        labels = {
            'name': 'Nome',
            'brand': 'Marca',
            'category': 'Categoria',
            'description': 'Descrição',
            'cost_price': 'Preço de Custo',
            'selling_price': 'Preço de Venda',
            'barcode': 'Código de Barras',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        brand = self.cleaned_data.get('brand')
        if len(name) <= 3:
            raise forms.ValidationError('Nome muito curto, tente outro.')
        return name

    def clean_barcode(self):
        barcode = self.cleaned_data['barcode']
        if Product.objects.filter(barcode=barcode):
            raise forms.ValidationError('Produto com este código de barras já existe.')
        return barcode


class ProductUpdateForm(ProductForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) <= 3:
            raise forms.ValidationError('Nome muito curto, tente outro.')
        return name

    def clean_barcode(self):
        return self.cleaned_data['barcode']
