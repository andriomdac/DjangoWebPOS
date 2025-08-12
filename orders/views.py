from django.shortcuts import render, redirect
from django.http import HttpResponse
from orders.models import Order, OrderItem
from icecream import ic
from django.shortcuts import get_object_or_404
from sales.models import Sale, SaleItem
from sales.utils import handle_sale_id_in_session
from orders.utils import is_there_active_orders
from django.contrib import messages
from app.utils import add_pagination_to_view_context
from django.contrib.auth.decorators import permission_required, login_required


@login_required
@permission_required('products.view_product', raise_exception=True)
def orders_list_view(request):
    orders = Order.objects.filter(active=True)
    context = {}

    add_pagination_to_view_context(request, orders.order_by('-created_at'), context, 10)
    is_there_active_orders(request, context)
    handle_sale_id_in_session(request, context)
    return render(request, template_name='orders_list.html', context=context)

@login_required
@permission_required('products.delete_product', raise_exception=True)
def finished_orders_list_view(request):
    orders = Order.objects.filter(active=False)
    context = {}

    add_pagination_to_view_context(request, orders.order_by('-created_at'), context, 10)
    is_there_active_orders(request, context)
    handle_sale_id_in_session(request, context)
    return render(request, template_name='finished_orders_list.html', context=context)

@login_required
@permission_required('products.delete_product', raise_exception=True)
def deactivate_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.active = False
    order.save()
    return redirect('orders_list')

@login_required
@permission_required('products.view_product', raise_exception=True)
def accept_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.products.all()
    
    if 'sale_id' in request.session:
        handle_sale_id_in_session(request, context)
        return redirect('order_detail', order_id)
    new_sale = Sale.objects.create()
    sale_total_price = 0
    for item in order_items:
        if item.quantity <= item.product.quantity:  
            new_sale_item = SaleItem.objects.create(
                sale=new_sale,
                product=item.product,
                quantity=item.quantity,
                price=item.product.selling_price,
                total_price=item.product.selling_price * item.quantity
            )
            sale_total_price += new_sale_item.total_price
        else:
            messages.warning(request, f"""Estoque insuficiente do produto {item.product.name} para esse pedido.
            Quantidade requisitada: {item.quantity} / Estoque atual: {item.product.quantity}""", extra_tags='danger')
            new_sale.delete()
            return redirect('orders_list')

    if not 'sale_id' in request.session:
        new_sale.total = sale_total_price
        new_sale.save()
        request.session['sale_id'] = new_sale.pk

    order.active = False
    order.save()
    return redirect('start_sale')

@login_required
@permission_required('products.view_product', raise_exception=True)
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items_quantity = order.products.all().count()
    order_items = order.products.all()
    order_items_total_value = 0
    context = {}

    for item in order_items:
        order_items_total_value += item.product.selling_price * item.quantity

    if request.method == 'POST':
        if 'accept_order' in request.POST:
            accept_order(request, order.pk)
        if 'refuse_order' in request.POST:
            deactivate_order(request, order_id)

    context['order'] = order
    context['order_items'] = order_items
    context['total_value'] = order_items_total_value

    return render(request, template_name='order_detail.html', context=context)