from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Outflow
from .forms import OutflowCreateForm
from products.models import Product
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from orders.utils import is_there_active_orders
from app.utils import add_pagination_to_view_context
from django.contrib.auth.decorators import permission_required, login_required


@login_required
@permission_required('products.view_product', raise_exception=True)
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
                    Estoque: {product.quantity}''', extra_tags='danger')
                return redirect('outflow_create', pk=pk)
            outflow.save()
            messages.success(
                request,
                f'''Saída de {outflow.quantity}
                unidade(s) do produto "{product.name}"
                registrada.''')
            return redirect('product_list')
    return render(
        request,
        template_name='outflow_create.html',
        context={
            'form': form,
            'product': product
            })


@login_required
@permission_required('products.delete_product', login_url='/products/list')
def outflow_list_view(request):
    search = request.GET.get('search')
    outflows = Outflow.objects.all().order_by('-created_at')
    context = {}

    if search:
        outflows = outflows.filter(product__name__icontains=search)

    add_pagination_to_view_context(request, outflows, context, 10)
    is_there_active_orders(request, context)
    return render(request, 'outflow_list.html', context)


class OutflowDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Outflow
    template_name = 'outflow_detail.html'
    context_object_name = 'outflow'
    permission_required = 'products.delete_product'
