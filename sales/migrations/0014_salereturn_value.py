# Generated by Django 5.1.3 on 2024-12-28 20:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0013_salereturn'),
    ]

    operations = [
        migrations.AddField(
            model_name='salereturn',
            name='value',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01, message='O valor deve ser maior que zero.')]),
        ),
    ]
