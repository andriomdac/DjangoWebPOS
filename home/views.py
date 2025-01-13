from django.shortcuts import render
from sales.models import Sale, SaleItemReturn, SaleItem
from datetime import date, datetime
from django.db.models import Sum, F
from products.models import Product
from django.contrib.auth.decorators import login_required, permission_required


@login_required()
def dashboard_view(request):
    # Get query_date from request, default to today
    query_date_str = request.GET.get('query_date')  # Adjusted to match the GET method
    try:
        if query_date_str:
            query_date = datetime.strptime(query_date_str, '%Y-%m-%d').date()
        else:
            query_date = date.today()
    except ValueError:
        query_date = date.today()  # Fallback to today if parsing fails

    # Sales data for the selected date
    sales_today = Sale.objects.filter(created_at__date=query_date)
    sales_total_value = sum([sale.total for sale in sales_today])
    num_sales_today = sales_today.count()
    num_items_sold_today = SaleItem.objects.filter(
        sale__in=sales_today
        ).aggregate(
            total_items=Sum('quantity')
            )['total_items'] or 0

    # Returns and profit
    returns_total_value = SaleItemReturn.objects.filter(created_at__date=query_date).aggregate(
        total_value=Sum('value'))['total_value'] or 0.00
    profit_today = SaleItem.objects.filter(sale__in=sales_today).annotate(
        profit=F('quantity') * (F('product__selling_price') - F('product__cost_price'))
    ).aggregate(total_profit=Sum('profit'))['total_profit'] or 0.00

    # Top selling product
    top_selling_product = SaleItem.objects.filter(sale__in=sales_today) \
        .values('product__name') \
        .annotate(total_quantity=Sum('quantity')) \
        .order_by('-total_quantity') \
        .first()

    # Stock summary
    total_stock_value = Product.objects.aggregate(
        total_value=Sum(F('cost_price') * F('quantity'))
    )['total_value'] or 0.00
    total_stock_profit = Product.objects.aggregate(
        total_profit=Sum((F('selling_price') - F('cost_price')) * F('quantity'))
    )['total_profit'] or 0.00

    # Context data for the template
    context = {
        'sales_total_value': sales_total_value,
        'num_sales_today': num_sales_today,
        'num_items_sold_today': num_items_sold_today,
        'returns_total_value': returns_total_value,
        'top_selling_product': top_selling_product,
        'profit_today': profit_today,
        'total_stock_value': total_stock_value,
        'total_stock_profit': total_stock_profit,
        'query_date': query_date,
    }

    return render(request, 'dashboard.html', context)
