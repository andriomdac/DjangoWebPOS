from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Inflow
from .forms import InflowCreateForm
from products.models import Product
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


@login_required
@permission_required(['inflows.add_inflow'])
@transaction.atomic
def inflow_create_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = InflowCreateForm()
    if request.method == 'POST':
        form = InflowCreateForm(request.POST)
        if form.is_valid():
            inflow = form.save(commit=False)
            inflow.product = product
            inflow.save()
            messages.success(
                request,
                f'''Entrada de {inflow.quantity}
                    unidade(s) do produto "{product.name} - {product.brand}"
                    registrada.''')
            return redirect('product_list')
    return render(
        request,
        template_name='inflow_create.html',
        context={
            'form': form,
            'product': product
            })


class InflowListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Inflow
    template_name = 'inflow_list.html'
    context_object_name = 'inflows'
    ordering = ['-created_at']
    paginate_by = 20
    permission_required = 'inflows.view_inflow'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(product__name__icontains=search)
        return queryset


class InflowDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Inflow
    template_name = 'inflow_detail.html'
    context_object_name = 'inflow'
    permission_required = 'inflows.view_inflow'
