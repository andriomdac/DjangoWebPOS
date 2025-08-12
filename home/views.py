from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from sales.models import Sale, SaleItem
from datetime import datetime
from app.utils import add_pagination_to_view_context
from icecream import ic
from django.contrib.auth.decorators import permission_required, login_required
from sales.utils import clean_empty_sales
from sales.utils import handle_sale_id_in_session


def is_this_sale_in_session(request, sale):
    if 'sale_id' in request.session:
        if sale.pk == request.session['sale_id']:
            return True
        return False
    return False

@login_required
def dashboard_view(request):
    if request.user.has_perm('products.delete_product'):
        clean_empty_sales(request)
        content = {}
        handle_sale_id_in_session(request, content)
        # Set default date to today
        date = datetime.today().date()

        # If a custom dashboard date is stored in the session, use it
        if 'dashboard_date' in request.session:
            date_string = request.session['dashboard_date']
            if date_string:
                date = datetime.strptime(date_string, '%Y-%m-%d').date()

        content["date"] = date

        # Handle POST request (form submission)
        if request.method == 'POST':

            # Update session with a custom selected date
            if 'date' in request.POST:
                date_string = request.POST['date']
                if date_string:
                    request.session['dashboard_date'] = date_string
                    return redirect('dashboard')

            # Filter by day
            if 'day' in request.POST:
                request.session['date_type'] = 'day'
                sales = Sale.objects.filter(
                    created_at__day=date.day,
                    created_at__month=date.month,
                    created_at__year=date.year
                )

            # Filter by month
            if 'month' in request.POST:
                request.session['date_type'] = 'month'
                sales = Sale.objects.filter(
                    created_at__month=date.month,
                    created_at__year=date.year
                )

            # Filter by year
            if 'year' in request.POST:
                request.session['date_type'] = 'year'
                sales = Sale.objects.filter(
                    created_at__year=date.year
                )

            # Reset to today's date and remove date_type filter
            if 'today' in request.POST:
                today_date_str = datetime.today().date().strftime('%Y-%m-%d')
                request.session['dashboard_date'] = today_date_str
                if request.session.get('date_type'):
                    del request.session['date_type']
                return redirect('dashboard')

            # Default filter if no specific option selected
            else:
                sales = Sale.objects.filter(created_at__date=date)

        else:
            # GET request: default filter by exact date
            sales = Sale.objects.filter(created_at__date=date)

        # Reapply stored date_type filter from session, if any
        if 'date_type' in request.session:
            date_type = request.session['date_type']

            if date_type == 'day':
                sales = Sale.objects.filter(created_at__day=date.day)
            if date_type == 'month':
                sales = Sale.objects.filter(created_at__month=date.month)
            if date_type == 'year':
                sales = Sale.objects.filter(created_at__year=date.year)

            content['date_type'] = date_type

        # Initialize dashboard metrics
        content["sales_quantity"] = sales.count()
        content["total_value_sold"] = 0
        content["total_profit"] = 0
        content["sales"] = sales

        discounts = 0  # Accumulator for total discounts

        # Iterate through sales to calculate totals
        for sale in sales:
            if is_this_sale_in_session(request, sale):
                continue

            sale_raw_total = 0

            # Sum up raw total from all sale items (without discounts)
            for item in sale.items.all():
                sale_raw_total += item.total_price

            sale_total_with_discounts = 0

            # Sum the actual total received, considering discounts
            for method in sale.payment_methods.all():
                sale_total_with_discounts += method.value

            # Calculate and accumulate the discount amount
            discounts += sale_raw_total - sale_total_with_discounts

            # Calculate profit for each item sold
            for sale_item in sale.items.all():
                content['total_profit'] += (sale_item.product.selling_price - sale_item.product.cost_price) * sale_item.quantity

            # Add to total revenue
            content['total_value_sold'] += sale.total

            # Accumulate values by payment method
            for payment_method in sale.payment_methods.all():
                if payment_method.method_name not in content:
                    content[payment_method.method_name] = 0
                content[payment_method.method_name] += payment_method.value

        # Final profit adjusted by total discounts
        content['total_profit'] -= discounts

        # Add pagination to the sales list (20 per page)
        add_pagination_to_view_context(
            request,
            object_list=sales.order_by('-created_at'),
            context=content,
            per_page=20
        )

        # Render the dashboard template with calculated data
        return render(request, template_name='dashboard.html', context=content)
    else:
        return redirect('product_list')
