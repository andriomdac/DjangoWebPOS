# Generated by Django 5.1.3 on 2025-02-14 00:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inflows', '0002_alter_inflow_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inflow',
            name='quantity',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
