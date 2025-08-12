

def handle_sale_id_in_session(request, context):
    """
    Verify whether pending/active sale in session has items or not,
    if it doesn't, delete 'sale_id' from session, otherwise do nothing.
    """
    from django.contrib import messages
    from django.shortcuts import render
    from sales.models import Sale

    sale_id = request.session.get('sale_id')

    if sale_id:
        context['sale_id'] = request.session['sale_id']
        try:
            sale = Sale.objects.get(id=sale_id)
            if sale.items.exists():
                context['active_sale'] = sale_id
                messages.warning(request, """❗️❗️ Existe uma venda em aberto,
                finalize-a para criar uma outra.❗️❗️""")
            else:
                sale.delete()
                del request.session['sale_id']
        except Sale.DoesNotExist:
            del request.session['sale_id']


def clean_empty_sales(request):
    """
    Delete all sales without any payment methods assigned to it, and with total zero (total)
    """
    from sales.models import Sale
    from django.shortcuts import get_list_or_404
    from icecream import ic

    empty_sales = Sale.objects.filter(total=0)
    if empty_sales:
        for sale in empty_sales:
            if 'sale_id' in request.session:
                session_sale_id = request.session['sale_id']
                if sale.pk == session_sale_id:
                    continue
            sale.delete()
            