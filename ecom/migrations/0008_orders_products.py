# Generated by Django 4.2.8 on 2023-12-31 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0007_remove_orders_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='products',
            field=models.TextField(default=897),
            preserve_default=False,
        ),
    ]
