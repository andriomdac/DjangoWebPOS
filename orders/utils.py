def is_there_active_orders(request, context):
    from orders.models import Order
    
    orders = Order.objects.filter(active=True)
    if orders:
        context['active_orders'] = orders.count()
        return True
    return False