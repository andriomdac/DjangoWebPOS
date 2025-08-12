from django import forms
from .models import Category
from django.core.exceptions import ValidationError

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category",]

        widgets = {"category": forms.TextInput(attrs={"class": "form-control", "autofocus": ""})}

    def clean_category(self):
        data = self.cleaned_data['category']
        if Category.objects.filter(category=data).exists():
            raise ValidationError('Já existe uma categoria com esse nome.')
        return data