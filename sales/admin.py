from django.contrib import admin
from .models import PaymentMethod, Sale, SaleItem

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ["method",]
    search_fields = ["method",]

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ["total", "created_at", "updated_at", "payment_method",]
    search_fields = ["total",]
    
@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ["sale", "product", "quantity", "price",]
    search_fields = ["product",]