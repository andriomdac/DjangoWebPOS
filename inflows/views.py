from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Inflow
from .forms import InflowCreateForm
from products.models import Product
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from orders.utils import is_there_active_orders
from app.utils import add_pagination_to_view_context
from django.contrib.auth.decorators import permission_required, login_required


@login_required
@permission_required('products.delete_product', raise_exception=True)
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
                    unidade(s) do produto "{product.name}"
                    registrada.''')
            return redirect('product_list')
    context = {
            'form': form,
            'product': product
            }
    return render(
        request,
        template_name='inflow_create.html',
        context=context)


@login_required
@permission_required('products.delete_product', login_url='/products/list')
def inflow_list_view(request):
    search = request.GET.get('search')
    inflows = Inflow.objects.all().order_by('-created_at')
    context = {}

    if search:
        inflows = inflows.filter(product__name__icontains=search)

    add_pagination_to_view_context(request, inflows, context, 10)
    is_there_active_orders(request, context)
    return render(request, 'inflow_list.html', context)


class InflowDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Inflow
    template_name = 'inflow_detail.html'
    context_object_name = 'inflow'
    permission_required = 'products.delete_product'
