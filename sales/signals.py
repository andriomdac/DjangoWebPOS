from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import SaleItem, SaleItemReturn
from products.models import Product


@receiver(signal=post_save, sender=SaleItem)
def sale_item_post_save(sender, instance, created, **kwargs):
    if created:
        item_quantity = instance.quantity
        product = instance.product
        product.quantity -= item_quantity
        product.save()

@receiver(signal=post_delete, sender=SaleItem)
def sale_item_post_delete(sender, instance, **kwargs):
    item_quantity = instance.quantity
    product = instance.product
    product.quantity += item_quantity
    product.save()

@receiver(signal=post_save, sender=SaleItemReturn)
def sale_item_return_post_save(sender, created, instance, **kwargs):
    if created:
        product = instance.product
        product.quantity += instance.quantity
        product.save()
    