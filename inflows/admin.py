from django.contrib import admin
from .models import Inflow


@admin.register(Inflow)
class InflowAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'created_at', 'updated_at',]
    search_fields = ['created_at',]
