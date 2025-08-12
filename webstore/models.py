from django.db import models
from django.core.validators import MinValueValidator


class SellerWhatsappNumber(models.Model):
    seller_name = models.CharField(max_length=100)
    whatsapp_number = models.IntegerField(
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Valor não pode ser menor que 1.'
            )
        ])
    
    def __str__(self):
        return f"{self.whatsapp_number}"
