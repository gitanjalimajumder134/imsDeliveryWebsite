# Generated by Django 3.2 on 2023-07-05 05:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0045_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quantity',
            name='Quantity',
        ),
    ]
