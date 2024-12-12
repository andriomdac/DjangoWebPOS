from django.db import models
from brands.models import Brand
from categories.models import Category


class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(to=Brand, on_delete=models.PROTECT, related_name='brand')
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT, related_name='category')
    description = models.TextField(max_length=500, blank=True, null=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    barcode = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.name