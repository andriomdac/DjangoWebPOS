from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DetailView
from .models import Product
from .forms import ProductForm, ProductUpdateForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError
from sales.models import SaleItemReturn
from sales.forms import SaleItemReturnForm
from sales.models import Sale, SaleItem
from django.db import transaction
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from app.utils import add_pagination_to_view_context


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    template_name = 'product_create.html'
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    permission_required = 'products.add_product'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Produto "{self.object.name}" adicionado com sucesso!'
            )
        return response


@login_required
@permission_required(['products.view_product'])
def product_list_view(request):
    products = Product.objects.all()
    search = request.GET.get('search')

    if search:
        try:
            search = int(search)
            products = products.filter(barcode__contains=search)
        except TypeError:
            products = products.filter(name__contains=search)
        except ValueError:
            products = products.filter(name__contains=search)
    context = {
        'products': products,
    }

    add_pagination_to_view_context(
        request,
        object_list=products,
        context=context,
        per_page=20
        )

    if 'sale_id' in request.session:
        context['sale_id'] = request.session['sale_id']
        sale = get_object_or_404(Sale, id=context['sale_id'])
        if sale.items.all().count() > 0:
            context['active_sale'] = request.session['sale_id']
            messages.warning(request, "Existe uma venda em aberto")
            return render(request, 'product_list.html', context)
        else:
            sale.delete()
            del request.session['sale_id']

    return render(request, 'product_list.html', context)


@login_required
@permission_required(['sales.add_sale'])
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
    permission_required = 'products.change_product'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Produto "{self.object.name}" alterado com sucesso!')
        return response


@login_required
@permission_required(['products.delete_product'])
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


@login_required
@permission_required(['sales.add_sale'])
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

    if 'sale_id' in request.session:
        context['sale_id'] = request.session['sale_id']

    return render(request, template_name='product_return_form.html', context=context)


@login_required
@permission_required(['sales.add_sale'])
def product_return_list_view(request):
    product_list = SaleItemReturn.objects.all().order_by('-created_at')
    context = {
        'product_list': product_list,
    }
    return render(request, template_name="product_return_list.html", context=context)
