# Generated by Django 3.2 on 2023-10-13 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0099_order_deliverydate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='deliverydate',
        ),
    ]
