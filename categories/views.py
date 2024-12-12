from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from .models import Category
from .forms import CategoryForm, CategoryUpdateForm
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from django.contrib import messages


class CategoryCreateView(CreateView):
    model = Category
    template_name = 'category_create.html'
    form_class = CategoryForm
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Categoria {self.object.name} criada com sucesso!')
        return response


class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        return context


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'category_create.html'
    form_class = CategoryUpdateForm
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Categoria "{self.object.name}" alterada com sucesso!')
        return response


def category_delete_view(request, pk):
    category_object = get_object_or_404(Category, id=pk)
    if request.method == 'POST':
        try: 
            category_object.delete()
            messages.success(request, f'Categoria "{category_object.name}" deletada com sucesso!')
            return redirect('category_list')
        except ProtectedError:
            return render(request, template_name='category_delete.html', context={
                'object': category_object,
                'message': f'Não é possível deletar a categoria "{category_object.name}", pois está sendo utilizada por um ou mais produtos'
                })
    return render(request, template_name='category_delete.html', context={'object': category_object})


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'