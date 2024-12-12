from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from .models import Product
from .forms import ProductForm, ProductUpdateForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError


class ProductCreateView(CreateView):
    model = Product
    template_name = 'product_create.html'
    form_class = ProductForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Produto "{self.object.name}" adicionado com sucesso!')
        return response


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product_update.html'
    form_class = ProductUpdateForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Produto "{self.object.name}" alterado com sucesso!')
        return response


def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        try:
            product.delete()
            messages.success(request, f'Produto "{product.name}" deletado com sucesso!')
            return redirect('product_list')
        except ProtectedError:
            return render(request, template_name='product_delete.html', context={
                'object': product,
                'message': f'Não foi possível deletar o produto "{product.name}", pois ele está sendo utilizado em uma ou mais vendas passadas.'
            })
    return render(request, template_name='product_delete.html', context={'object': product})


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'