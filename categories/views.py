from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from .models import Category
from .forms import CategoryForm, CategoryUpdateForm
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Category
    template_name = 'category_create.html'
    form_class = CategoryForm
    success_url = reverse_lazy('category_list')
    permission_required = 'add_category'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Categoria "{self.object.name}" criada com sucesso!'
            )
        return response


class CategoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'
    paginate_by = 20
    permission_required = 'categories.view_category'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset


class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Category
    template_name = 'category_create.html'
    form_class = CategoryUpdateForm
    success_url = reverse_lazy('category_list')
    permission_required = 'categories.change_category'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Categoria "{self.object.name}" alterada com sucesso!'
            )
        return response


@login_required()
@permission_required(['categories.delete_category'])
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
                'message': f'''Não é possível deletar a categoria "{category_object.name}",
                            pois está sendo utilizada por um ou mais produtos'''
                })
    return render(
        request,
        template_name='category_delete.html',
        context={
            'object': category_object
            })


class CategoryDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'
    permission_required = 'categories.view_category'
