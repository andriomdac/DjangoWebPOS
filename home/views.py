from django.shortcuts import render
from sales.models import Sale, SaleItemReturn, SaleItem, PaymentMethod
from datetime import date
from django.db.models import Sum, F
from products.models import Product

def dashboard_view(request):
    # Sales for today
    today = date.today()
    sales_today = Sale.objects.filter(created_at__date=today)

    # Total Sales Value
    sales_total_value = sum([sale.total for sale in sales_today])

    # Number of Sales (daily)
    num_sales_today = sales_today.count()

    # Number of Items Sold (daily)
    num_items_sold_today = SaleItem.objects.filter(sale__in=sales_today).aggregate(total_items=Sum('quantity'))['total_items'] or 0

    # Total Value of Returns (daily)
    returns_total_value = SaleItemReturn.objects.filter(created_at__icontains=date.today()).aggregate(total_value=Sum('value'))['total_value'] or 0.00

    # Top-selling Product (daily)
    top_selling_product = SaleItem.objects.filter(sale__in=sales_today) \
        .values('product__name') \
        .annotate(total_quantity=Sum('quantity')) \
        .order_by('-total_quantity') \
        .first()

    # Profit (daily)
    profit_today = SaleItem.objects.filter(sale__in=sales_today) \
        .annotate(profit=F('quantity') * (F('product__selling_price') - F('product__cost_price'))) \
        .aggregate(total_profit=Sum('profit'))['total_profit'] or 0.00

    # Total value of current stock (sum of cost_price * quantity)
    total_stock_value = Product.objects.aggregate(
        total_value=Sum(F('cost_price') * F('quantity'))
    )['total_value'] or 0.00

    # Total profit of current stock (sum of (selling_price - cost_price) * quantity)
    total_stock_profit = Product.objects.aggregate(
        total_profit=Sum((F('selling_price') - F('cost_price')) * F('quantity'))
    )['total_profit'] or 0.00

    # Get today's date
    today_date = date.today()

    # Add to context
    context = {
        'sales_total_value': sales_total_value,
        'num_sales_today': num_sales_today,
        'num_items_sold_today': num_items_sold_today,
        'returns_total_value': returns_total_value,
        'top_selling_product': top_selling_product,
        'profit_today': profit_today,
        'total_stock_value': total_stock_value,
        'total_stock_profit': total_stock_profit,
        'today_date': today_date,  # Adding today's date to the context
    }

    return render(request, template_name='dashboard.html', context=context)