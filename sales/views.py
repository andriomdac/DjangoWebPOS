from django.shortcuts import render, get_object_or_404, redirect
from .models import Sale, SaleItem
from .forms import SaleItemForm, PaymentMethodForm
from django.views.generic import ListView
from django.urls import reverse_lazy
from products.models import Product


class SaleListView(ListView):
    model = Sale
    template_name = 'sale_list.html'
    context_object_name = 'sales'


def sale_view(request):
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
                sale_item.product = product
                sale_item.sale = sale
                sale_item.price = product.selling_price
                sale_item.total_price = sale_item.price * sale_item.quantity
                sale_item.save()
                return redirect('start_sale')
            except Product.DoesNotExist:
                form.add_error('barcode', 'Produto com esse código de barras não existe.')
        else:
            form = SaleItemForm(request.POST)
    else:
        form = SaleItemForm()

    sale_items = sale.items.all()
    sale_total_price = sum([item.total_price for item in sale_items])
    sale.total = sale_total_price
    sale.save()

    return render(request, template_name='sale_create.html', context={
        'form': form,
        'sale_items': sale_items,
        'sale_total': sale_total_price,
        })


def sale_finalize_view(request):
    sale = get_object_or_404(Sale, id=request.session['sale_id'])

    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            payment_method = form.save(commit=False)
            payment_method.sale = sale
            payment_method.save()
            return redirect('sale_finalize')

    else:
        form = PaymentMethodForm()

    sale_payments = sale.payment_methods.all()
    total_paid = sum([payment.value for payment in sale_payments])
    total_payable = sale.total - total_paid

    return render(request, 'sale_finalize.html', context={
        'sale': sale,
        'sale_payments': sale_payments,
        'form': form,
        'total_payable': total_payable,
        'total_paid': total_paid,
        'total_payable': total_payable
    })

    

