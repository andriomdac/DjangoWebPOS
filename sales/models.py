from django.db import models
from products.models import Product
from django.core.validators import MinValueValidator


PAYMENT_METHOD_CHOICES = (
    ("PIX", "PIX"),
    ("CARTÃO", "CARTÃO"),
    ("DINHEIRO", "DINHEIRO"),
    )


class Sale(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"""Venda {self.id} -
        Total: R${self.total:.2f} ({self.items.count()} itens
        em {self.created_at}"""


class SaleItem(models.Model):
    sale = models.ForeignKey(to=Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        to=Product,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='product_items'
        )
    quantity = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(
                1,
                message="A quantidade deve ser maior que zero"
                )])
    price = models.DecimalField(
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(
                0.01,
                message="O preço deve ser maior que zero"
                )]
        )
    total_price = models.DecimalField(
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(
                0.01,
                message="O preço total deve ser maior que zero."
                )]
        )

    def __str__(self):
        return f"{self.sale.id}"


class PaymentMethod(models.Model):
    sale = models.ForeignKey(
        to=Sale,
        on_delete=models.CASCADE,
        related_name='payment_methods',
        default=1
        )
    method_name = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES
        )
    value = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0.00,
        validators=[MinValueValidator(0.01, message='O valor deve ser maior que zero.')]
        )

    def __str__(self):
        return self.method_name


class SaleItemReturn(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='returns')
    quantity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1, message="A quantidade deve ser maior que zero")]
        )
    value = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0.00,
        validators=[MinValueValidator(0.01, message='O valor deve ser maior que zero.')]
        )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
