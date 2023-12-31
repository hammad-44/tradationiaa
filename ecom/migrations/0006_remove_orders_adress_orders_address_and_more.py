# Generated by Django 4.2.8 on 2023-12-31 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0005_orders'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='adress',
        ),
        migrations.AddField(
            model_name='orders',
            name='address',
            field=models.TextField(default=121),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orders',
            name='products',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='orders',
            name='total',
            field=models.PositiveIntegerField(),
        ),
    ]
