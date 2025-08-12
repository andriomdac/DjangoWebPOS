from django.shortcuts import render, redirect
from products.models import Product
from categories.models import Category
from django.shortcuts import get_object_or_404
from django.contrib import messages
from icecream import ic
from django.http import HttpResponse
from .utils import  (
    generate_link_for_cart_message,
    generate_link_for_direct_order_message,
    add_product_to_cart
    )
from django.contrib.auth.decorators import login_not_required


@login_not_required
def webstore_home_view(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        "products": products,
        "categories": categories,
        "cart_quantity": len(request.session.get('cart', [])),
    }

    if request.method == 'POST':
        if 'search' in request.POST:
            search = request.POST['search']
            context['products'] = Product.objects.filter(name__icontains=search)
        if 'category' in request.POST:
            category = get_object_or_404(Category, id=int(request.POST['category']))
            context['products'] = Product.objects.filter(category=category)
        if 'direct_order' in request.POST:
            link = generate_link_for_direct_order_message(request, product_id=int(request.POST['direct_order']))
            return redirect(link)
        if 'add_product_to_cart' in request.POST:
            add_product_to_cart(request)
            return redirect('webstore_home')

    return render(request, template_name='webstore_home.html', context=context)


@login_not_required
def webstore_cart_view(request):
    if request.method == 'POST':
        if 'delete_product' in request.POST:
            cart = request.session.get('cart', [])
            product_id = int(request.POST['delete_product'])
            cart.remove(product_id)
            request.session['cart'] = cart
        if 'confirm_cart_purchase' in request.POST:
            link = generate_link_for_cart_message(request=request)
            return redirect(link)
      
    products_obj = [get_object_or_404(Product, id=id) for id in request.session.get('cart', [])]
    products_quantity_json = {}
    products_total_value = 0
    for product in products_obj:
        if product not in products_quantity_json:
            products_quantity_json[product] = 1
        else:
            products_quantity_json[product] += 1
        products_total_value += product.selling_price
    
    context = {
        'products': products_quantity_json,
        'total': products_total_value
        }
    return render(request, template_name='webstore_cart.html', context=context)