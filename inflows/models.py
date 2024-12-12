from django.db import models
from products.models import Product
from django.core.validators import MinValueValidator


class Inflow(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, related_name='products')
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.created_at}'