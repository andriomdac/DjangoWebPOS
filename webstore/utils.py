from icecream import ic


SELLER_WHATSAPP_NUMBER = 5577998529178
SITE_LINK = "https://jlsuplementos.caverna.lat/orders/detail/"


def generate_link_for_direct_order_message(request, product_id):
    from django.shortcuts import get_object_or_404
    from products.models import Product       
    from orders.models import Order, OrderItem

    new_client_order = Order.objects.create()
    order_product = OrderItem.objects.create(
        product=get_object_or_404(Product, id=int(request.POST['direct_order'])),
        order=new_client_order
    )
    product = get_object_or_404(Product, id=product_id)

    # Text formatting for WhatsApp message
    message = (
        "Olá, gostaria de realizar a compra do produto:\n\n"
        f"➝ {product.name}\n"
        f"\n- Valor do pedido: R$ {product.selling_price}\n\n"
        f"Link: \n{SITE_LINK}{new_client_order.pk}/\n"
        f"Pedido nº{new_client_order.pk}"
    )


    link = f"https://wa.me/{SELLER_WHATSAPP_NUMBER}/?text={message}"
    return link


def add_product_to_cart(request):
    from django.shortcuts import get_object_or_404
    from products.models import Product
    from django.contrib import messages

    product = get_object_or_404(Product, id=int(request.POST['add_product_to_cart']))
    cart = request.session.get('cart', [])
    cart.append(product.pk)
    request.session['cart'] = cart
    return messages.info(request, f"Produto {product.name} adicionado ao carrinho.")


def generate_link_for_cart_message(request):
    from django.shortcuts import get_object_or_404
    from products.models import Product
    from orders.models import Order, OrderItem

    new_client_order = Order.objects.create()
    products_ids = request.session.get('cart', [])

    products_quantity = {}
    for id in products_ids:
        product = get_object_or_404(Product, id=id)
        if product in products_quantity:
            products_quantity[product] += 1
        else:
            products_quantity[product] = 1
    
    client_order_total_value = 0
    for product, quantity in products_quantity.items():
        client_order_total_value += product.selling_price * quantity
        order_product = OrderItem.objects.create(
            product=product,
            quantity=quantity,
            order=new_client_order
        )

    # Text formatting for WhatsApp message
    products_str = "\n".join(f"➝ ({v} unid.) *{k.name}*(R$ {k.selling_price * v})" for k, v in products_quantity.items())
    message = (
        "Olá, gostaria de realizar a compra dos seguintes produtos:\n\n"
        f"{products_str}\n"
        f"\n- Valor do pedido: R$ {client_order_total_value}\n\n"
        f"Link:\n*{SITE_LINK}{new_client_order.pk}/*\n"
        f"Pedido nº{new_client_order.pk}"
    )

    link = f"https://wa.me/{SELLER_WHATSAPP_NUMBER}/?text={message}"
    return link

