from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from .models import Product
from .forms import ProductForm, ProductUpdateForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError
from sales.models import SaleItemReturn
from sales.forms import SaleItemReturnForm


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

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset


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


def product_return_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = SaleItemReturnForm()

    if request.method == 'POST':
        form = SaleItemReturnForm(request.POST)
        if form.is_valid():
            return_form = form.save(commit=False)
            return_form.product = product
            return_form.value = product.selling_price
            return_form.save()
            messages.success(request, f"Devolução do item '{product.name}' realizada com sucesso.")
            return redirect('product_list')

    context = {
        'form': form,
        'product': product
    }
    return render(request, template_name='product_return.html', context=context)