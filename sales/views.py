from django.shortcuts import render, get_object_or_404, redirect
from .models import Sale, SaleItem
from .forms import SaleItemForm, PaymentMethodForm, PaymentMethod
from django.urls import reverse_lazy
from products.models import Product
from django.contrib import messages
from django.db import transaction
from decimal import Decimal


def sale_list_view(request):
    sales = Sale.objects.all().order_by('-created_at')  
    context = {'sales': sales}

    if 'sale_id' in request.session:
        sale = get_object_or_404(Sale, id=request.session['sale_id'])

        if sale.items.all().count() > 0:
            context['active_sale'] = request.session['sale_id']
            messages.warning(request, "Existe uma venda em aberto, finalize-a para criar uma nova")
            return render(request, 'sale_list.html', context)
        else:
            sale.delete()
            del request.session['sale_id']

    return render(request, 'sale_list.html', context)

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
                    messages.error(request, f'Estoque insuficiente do produto: {product.name}. Quantidade disponível: {product.quantity}')
                    return redirect('start_sale')
            except Product.DoesNotExist:
                form.add_error('barcode', 'Produto com esse código de barras não existe.')
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

@transaction.atomic
def sale_finalize_view(request):
    sale = get_object_or_404(Sale, id=request.session['sale_id'])
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)

        if request.POST.get("name") == "finalize":
            messages.success(request, message=f"Venda {request.session['sale_id']} realizada com sucesso!")
            del request.session['sale_id']
            return redirect('sale_list')
        
        if form.is_valid():
            payment_method = form.save(commit=False)
            payment_method.sale = sale
            payment_method.save()
            request.session['payment_method_id'] = payment_method.pk
            return redirect('sale_finalize')

    sale_payments = sale.payment_methods.all()
    form = PaymentMethodForm()
    total_paid = sum([payment.value for payment in sale_payments])
    total_payable = sale.total - total_paid
    sale_is_fully_paid = bool(total_payable <= 0)
    sale_has_change = bool(total_paid > sale.total)
    change = total_paid - sale.total

    if 'payment_method_id' in request.session:
        payment_method_id = request.session['payment_method_id']
    else:
        payment_method_id = None

    print(f'''Total Pago: {total_paid}
    Total a pagar: {total_payable}
    Venda está completamente paga: {sale_is_fully_paid}
    Venda tem troco: {sale_has_change}
    Troco do Cliente: {change}
    ID do método de pagamento: {payment_method_id}''')

    context = {
        'sale': sale,
        'sale_payments': sale_payments,
        'form': form,
        'total_payable': total_payable,
        'total_paid': total_paid,
        'sale_is_fully_paid': sale_is_fully_paid,
        'sale_has_change': sale_has_change,
        'change': change,
    }

    if sale_is_fully_paid:
        context['sale_is_fully_paid'] = sale_is_fully_paid

    return render(request, 'sale_finalize.html', context=context)


def sale_item_delete(request, pk):
    sale_item = get_object_or_404(SaleItem, id=pk)
    sale_item.delete()
    return redirect('start_sale')

def payment_method_delete(request, pk):
    payment_method = get_object_or_404(PaymentMethod, id=pk)
    payment_method.delete()
    return redirect('sale_finalize')

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