# Generated by Django 3.2 on 2022-11-28 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0023_order_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='quantity',
        ),
    ]