from django.db import models
from products.models import Product
from django.core.validators import MinValueValidator


class PaymentMethod(models.Model):
    method = models.CharField(max_length=20)

    def __str__(self):
        return self.method


class Sale(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_method = models.ForeignKey(
        to=PaymentMethod,
        on_delete=models.PROTECT,
        related_name='sales'
        )

    def __str__(self):
        return f"Venda {self.id} - Total: R${self.total:.2f} ({self.items.count()} itens) em {self.created_at}"


class SaleItem(models.Model):
    sale = models.ForeignKey(to=Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        to=Product,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='product_items'
        )
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1, message="A quantidade deve ser maior que zero")])
    price = models.DecimalField(
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01, message="O preço deve ser maior que zero")]
        )

    def __str__(self):
        return f"{self.quantity} x {self.product.name} - {self.sale.id}"

