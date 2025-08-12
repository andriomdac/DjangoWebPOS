from django.shortcuts import render, redirect
from .forms import CategoryForm
from django.http import HttpResponse
from django.contrib import messages
from .models import Category
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from orders.utils import is_there_active_orders
from django.contrib.auth.decorators import permission_required, login_required


@login_required
@permission_required('products.delete_product', raise_exception=True)
def category_add_view(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria adicionada com sucesso.')
            return redirect('category_list')
    context = {
        "form": form
    }
    if request.user.has_perm('products.delete_product'):
        context['has_perm'] = 'delete_product'
    return render(request, template_name='category_add.html', context=context)

@login_required
@permission_required('products.view_product', raise_exception=True)
def category_list_view(request):
    categories = Category.objects.all().order_by('category')
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        if request.user.has_perm('products.delete_product'):
            if 'category_delete_id' in request.POST:
                try:
                    get_object_or_404(Category, id=int(request.POST['category_delete_id'])).delete()
                    messages.success(request, 'Categoria deletada com sucesso.')
                    return redirect('category_list')
                except:
                    messages.error(request, 'Erro ao deletar. Categoria está sendo utilizada em algum produto', extra_tags='danger')
                    return redirect('category_list')
        else:
            messages.warning(request, 'Acesso Negado', extra_tags='danger')

    context = {
        "page_obj": page_obj,
        "paginator": paginator,
    }
    if request.user.has_perm('products.delete_product'):
        context['has_perm'] = 'delete_product'
    is_there_active_orders(request, context)
    return render(request, template_name='category_list.html', context=context)