# Generated by Django 5.1.3 on 2024-12-17 23:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_product_name'),
        ('sales', '0002_alter_sale_payment_method_alter_saleitem_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='product_items', to='products.product'),
        ),
    ]
