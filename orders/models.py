from django.db import models
from django.core.validators import MinValueValidator
from products.models import Product


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Order #{self.pk}"

class OrderItem(models.Model):
    product = models.ForeignKey(
        to=Product,
        on_delete=models.PROTECT
        )
    quantity = models.IntegerField(
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Valor não pode ser menor que 1.'
            )
            ],
        default=1
        )
    order = models.ForeignKey(
        to=Order,
        on_delete=models.PROTECT,
        related_name='products'
    )

    @property
    def total(self):
        return self.product.selling_price * self.quantity


    def __str__(self):
        return f"{self.product} - {self.quantity}und."