from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description",]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autofocus': ''}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
        }
        labels = {
            'name': 'Nome',
            'description': 'Descrição'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) <= 3:
            raise forms.ValidationError('Nome muito curto, tente outro.')
        if Category.objects.filter(name__icontains=name):
            raise forms.ValidationError('Já existe uma categoria com esse nome.')

        return name


class CategoryUpdateForm(CategoryForm):
    def clean_name(self):
        return self.cleaned_data['name']
