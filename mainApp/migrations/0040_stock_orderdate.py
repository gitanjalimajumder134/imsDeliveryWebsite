# Generated by Django 3.2 on 2023-02-01 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0039_stock_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='orderDate',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
