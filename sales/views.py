from django.shortcuts import render, get_object_or_404, redirect
from .models import Sale, SaleItem
from .forms import SaleItemForm, PaymentMethodForm, PaymentMethod
from products.models import Product
from django.contrib import messages
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from app.utils import add_pagination_to_view_context


@login_required
def sale_list_view(request):
    sales = Sale.objects.all().order_by('-created_at')
    context = {'sales': sales}

    add_pagination_to_view_context(request, object_list=sales, context=context)

    if 'sale_id' in request.session:
        sale = get_object_or_404(Sale, id=request.session['sale_id'])

        if sale.items.all().count() > 0:
            context['active_sale'] = request.session['sale_id']
            messages.warning(
                request,
                """Existe uma venda em aberto,
                finalize-a para criar uma nova"""
                )
            return render(request, 'sale_list.html', context)
        else:
            sale.delete()
            del request.session['sale_id']

    return render(request, 'sale_list.html', context)


@login_required
@transaction.atomic
def sale_cart_view(request):
    if not request.session.get('sale_id'):
        sale = Sale.objects.create()
        request.session['sale_id'] = sale.id
    else:
        sale = get_object_or_404(Sale, id=request.session['sale_id'])

    if request.method == 'POST':
        form = SaleItemForm(request.POST)
        if form.is_valid():
            barcode = form.cleaned_data.get('barcode')
            try:
                product = Product.objects.get(barcode=barcode)
                sale_item = form.save(commit=False)
                if sale_item.quantity <= product.quantity:
                    sale_item.product = product
                    sale_item.sale = sale
                    sale_item.price = product.selling_price
                    sale_item.total_price = sale_item.price * sale_item.quantity
                    sale_item.save()
                    return redirect('start_sale')
                else:
                    messages.error(
                        request,
                        f'''Estoque insuficiente do produto: {product.name}.
                        Quantidade disponível: {product.quantity}'''
                        )
                    return redirect('start_sale')
            except Product.DoesNotExist:
                form.add_error(
                    'barcode',
                    'Produto com esse código de barras não existe.'
                    )
        else:
            form = SaleItemForm(request.POST)
    else:
        form = SaleItemForm()

    sale_items = sale.items.all()
    sale_has_items = bool(sale_items)

    sale_total_price = sum([item.total_price for item in sale_items])
    sale.total = sale_total_price
    sale.save()

    return render(request, template_name='sale_create.html', context={
        'form': form,
        'sale_items': sale_items,
        'sale_total': sale_total_price,
        'sale_has_items': sale_has_items,
        })


@login_required
@transaction.atomic
def sale_finalize_view(request):
    sale = get_object_or_404(Sale, id=request.session['sale_id'])
    form = PaymentMethodForm()
    sale_payments = sale.payment_methods.all()
    total_paid = sum([payment.value for payment in sale_payments])

    if total_paid < sale.total:
        if 'change' in request.session:
            del request.session['change']

    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)

        if request.POST.get("name") == "finalize":
            messages.success(
                request,
                message=f"""Venda {request.session['sale_id']}
                realizada com sucesso!"""
                )
            del request.session['sale_id']
            return redirect('sale_list')

        if request.POST.get("name") == "discount":
            discount_value = Decimal(request.POST.get("value", 0))
            if discount_value > 0 and discount_value < sale.total:
                sale.total -= discount_value
                sale.save()
                messages.success(
                    request,
                    f"""Desconto de
                    R$ {discount_value:.2f}
                    atribuido à venda."""
                    )
            else:
                messages.error(
                    request,
                    """Entrada Inválida.
                    Valor deve ser maior que zero
                    e menor que o total da venda.""",
                    extra_tags="danger"
                    )
            return redirect('sale_finalize')

        if form.is_valid():

            payment_method = form.save(commit=False)
            payment_method.sale = sale
            payment_method.save()

            sale_payments = sale.payment_methods.all()
            total_paid = sum([payment.value for payment in sale_payments])

            if total_paid > sale.total:
                change = total_paid - sale.total
            else:
                change = None

            if change:
                payment_method.value -= change
                payment_method.save()
                messages.warning(request, f'Troco do Cliente: {change}')
                request.session['change'] = float(change)
            return redirect('sale_finalize')

    total_payable = sale.total - total_paid
    sale_is_fully_paid = bool(total_payable <= 0)

    context = {
        'sale': sale,
        'sale_payments': sale_payments,
        'form': form,
        'total_payable': total_payable,
        'total_paid': total_paid,
        'sale_is_fully_paid': sale_is_fully_paid,
    }

    if 'change' in request.session:
        context['change'] = request.session['change']

    if sale_is_fully_paid:
        context['sale_is_fully_paid'] = sale_is_fully_paid

    return render(request, 'sale_finalize.html', context=context)


@login_required
def sale_item_delete(request, pk):
    sale_item = get_object_or_404(SaleItem, id=pk)
    sale_item.delete()
    return redirect('start_sale')


@login_required
def payment_method_delete(request, pk):
    payment_method = get_object_or_404(PaymentMethod, id=pk)
    payment_method.delete()
    return redirect('sale_finalize')


@login_required
def sale_detail_view(request, pk):
    sale = get_object_or_404(Sale, id=pk)
    sale_items = sale.items.all()
    payment_methods = sale.payment_methods.all()

    context = {
        'sale': sale,
        'sale_items': sale_items,
        'payment_methods': payment_methods,
    }
    return render(request, template_name='sale_detail.html', context=context)
