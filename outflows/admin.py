from django.contrib import admin
from .models import Outflow


@admin.register(Outflow)
class OutflowAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'created_at', 'updated_at',]
    search_fields = ['created_at',]
