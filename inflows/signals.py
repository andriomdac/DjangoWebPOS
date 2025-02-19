from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Inflow


@receiver(signal=post_save, sender=Inflow)
def inflow_post_save(sender, instance, **kwargs):
    product = instance.product
    product.quantity += instance.quantity
    product.save()
