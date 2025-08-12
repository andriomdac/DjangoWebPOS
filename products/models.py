from django.db import models
from django_resized import ResizedImageField
from categories.models import Category
from django.core.validators import MinValueValidator

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500, blank=True, null=True)
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT, default=10, related_name='products')
    product_image = ResizedImageField(size=[1920, 1080], null=True, blank=True, upload_to='product_images/')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    barcode = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
