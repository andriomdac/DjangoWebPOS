from django.contrib import admin
from .models import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    search_fields = ["name",]
    list_display = ["name", "description", "updated_at", "created_at",]
