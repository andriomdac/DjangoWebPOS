from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Outflow
from .forms import OutflowCreateForm
from products.models import Product
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
@transaction.atomic
def outflow_create_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = OutflowCreateForm()
    if request.method == 'POST':
        form = OutflowCreateForm(request.POST)
        if form.is_valid():
            outflow = form.save(commit=False)
            outflow.product = product
            if product.quantity < outflow.quantity:
                messages.error(
                    request,
                    f'''Erro: Estoque insuficiente para essa saída.
                    Estoque: {product.quantity}', extra_tags='danger''')
                return redirect('outflow_create', pk=pk)
            outflow.save()
            messages.success(
                request,
                f'''Saída de {outflow.quantity}
                unidade(s) do produto "{product.name} - {product.brand}"
                registrada.''')
            return redirect('product_list')
    return render(
        request,
        template_name='outflow_create.html',
        context={
            'form': form,
            'product': product
            })


class OutflowListView(LoginRequiredMixin, ListView):
    model = Outflow
    template_name = 'outflow_list.html'
    context_object_name = 'outflows'
    ordering = ['-created_at']
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(product__name__icontains=search)
        return queryset


class OutflowDetailView(LoginRequiredMixin, DetailView):
    model = Outflow
    template_name = 'outflow_detail.html'
    context_object_name = 'outflow'
