# Generated by Django 5.1.3 on 2024-12-22 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0008_paymentmethod'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentmethod',
            name='value',
        ),
        migrations.AddField(
            model_name='sale',
            name='payment_method',
            field=models.ManyToManyField(to='sales.paymentmethod'),
        ),
    ]
