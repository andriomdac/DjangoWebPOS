def toggle_theme(request):
    from django.shortcuts import redirect

    try:
        if 'light' in request.session['theme']:
            request.session['theme'] = 'dark'
            request.session['toggle'] = 'off'
        else:
            request.session['theme'] = 'light'
            request.session['toggle'] = 'on'
    except KeyError:
        request.session['theme'] = 'light'
        request.session['toggle'] = 'on'

    return redirect(request.headers['referer'])


def toggle_sidebar(request):
    from django.shortcuts import redirect


    if 'sidebar' in request.session:
        del request.session['sidebar']
    else:
        request.session['sidebar'] = 'active'
    
    return redirect(request.headers['referer'])


def add_pagination_to_view_context(
    request,
    object_list,
    context,
    per_page=10
    ):
    from django.core.paginator import Paginator


    paginator = Paginator(object_list, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context['page_obj'] = page_obj
    context['paginator'] = paginator


def delete_sale_with_no_items(request):
    from sales.models import Sale
    from django.shortcuts import get_object_or_404


    if 'sale_id' in request.session:
        sale = get_object_or_404(Sale, id=request.session['sale_id'])
        if sale.items.all().count() == 0:
            sale.delete()
            del request.session['sale_id']
