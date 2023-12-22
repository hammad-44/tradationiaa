# Generated by Django 5.0 on 2023-12-22 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='clothproduct',
            name='colors',
            field=models.ManyToManyField(to='products.color'),
        ),
        migrations.AddField(
            model_name='clothproduct',
            name='sizes',
            field=models.ManyToManyField(to='products.size'),
        ),
    ]