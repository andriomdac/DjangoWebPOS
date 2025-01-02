from django.shortcuts import render
from sales.models import Sale, SaleItemReturn, SaleItem
from datetime import date


def dashboard_view(request):
    # Dados do dashboard: 
        # Quantidade de vendas e produtos vendidos por dia
        # Valor de venda bruto e lucro (considerando devoluções de produto)
        # Valor bruto do estoque

    sales = Sale.objects.filter(created_at__icontains=date.today()) #Quantidade de Vendas por dia
    sold_sale_items = SaleItem() #Quantidade de produtos vendidos
    
    sales_total_value = sum([sale.total for sale in sales])
    

    context = {
        'sales_total_value': sales_total_value,
    }

    return render(request, template_name='dashboard.html', context=context)