from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DetailView
from .models import Product
from .forms import ProductForm, ProductUpdateForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError
from sales.models import Sale, SaleItem
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from app.utils import add_pagination_to_view_context
from categories.models import Category
from sales.utils import handle_sale_id_in_session
from orders.utils import is_there_active_orders
from django.contrib.auth.decorators import permission_required, login_required


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    template_name = 'product_create.html'
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    permission_required = 'products.delete_product'

    def form_valid(self, form):
        form.instance.product_image = self.request.FILES.get('product_image')
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Produto "{self.object.name}" adicionado com sucesso!'
        )
        return response

@login_required
@permission_required('products.view_product', raise_exception=True)
def product_list_view(request):
    products = Product.objects.all()
    search = request.GET.get('search')
    category_id = request.GET.get('category')

    if search:
        try:
            search_int = int(search)
            products = products.filter(barcode__icontains=search_int)
        except (TypeError, ValueError):
            products = products.filter(name__icontains=search)

    if category_id:
        products = products.filter(category__id=category_id)

    context = {
        'products': products,
    }

    add_pagination_to_view_context(
        request,
        object_list=products.order_by('name'),
        context=context,
        per_page=20
    )

    handle_sale_id_in_session(request, context)
    is_there_active_orders(request, context)

    categories = Category.objects.all()
    context['categories'] = categories
    if request.user.has_perm('products.delete_product'):
        context['has_perm'] = 'delete_product'
    return render(request, 'product_list.html', context)



@login_required
@permission_required('products.view_product', raise_exception=True)
@transaction.atomic
def product_item_add_to_sale(request, pk):
    if not request.session.get('sale_id'):
        sale = Sale.objects.create()
        request.session['sale_id'] = sale.id
    else:
        sale = get_object_or_404(Sale, id=request.session['sale_id'])

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                messages.error(request, "A quantidade deve ser maior ou igual a 1.")
                return redirect('product_list')
            if quantity > product.quantity:
                messages.error(
                    request,
                    f'''Erro: Estoque indisponível para essa quantidade.
                        Estoque: {product.quantity}''',
                    extra_tags='danger'
                    )

                return redirect('product_list')

            price = product.selling_price
            total_price = quantity * price

            SaleItem.objects.create(
                sale=sale,
                product=product,
                quantity=quantity,
                price=price,
                total_price=total_price
            )

            messages.success(request, f"Produto '{product.name}' adicionado à venda com sucesso!")
            return redirect('product_list')

        except ValueError:
            messages.error(request, "Quantidade inválida.")
            return redirect('product_list')

    else:
        messages.error(request, "Método de requisição inválido.")
        return redirect('product_list')


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    template_name = 'product_update.html'
    form_class = ProductUpdateForm
    success_url = reverse_lazy('product_list')
    permission_required = 'products.delete_product'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Produto "{self.object.name}" alterado com sucesso!')
        return response



@login_required
@permission_required('products.delete_product', raise_exception=True)
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
                'message': f'''Não foi possível deletar o produto "{product.name}",
                                pois ele está sendo utilizado em uma ou mais vendas passadas.'''
            })
    return render(request, template_name='product_delete.html', context={'object': product})


class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'
    permission_required = 'products.view_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.has_perm('products.delete_product'):
            context['has_perm'] = 'delete_product'
        return context
