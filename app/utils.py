
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