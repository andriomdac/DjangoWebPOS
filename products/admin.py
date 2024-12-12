from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ["name",]
    list_display = ["name", "brand", "category", "description", "created_at", "updated_at",]