# Generated by Django 5.1.3 on 2024-12-31 02:32

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0017_alter_paymentmethod_sale'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleitemreturn',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
