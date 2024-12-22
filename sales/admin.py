from django.contrib import admin
from .models import Sale, SaleItem, PaymentMethod


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ["total", "created_at", "updated_at",]
    search_fields = ["total",]


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ["sale", "product", "quantity", "price",]
    search_fields = ["product",]


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ["sale", "method_name", "value",]
    search_fields = ["method_name",]