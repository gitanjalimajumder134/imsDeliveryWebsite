# Generated by Django 3.2 on 2022-11-28 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0024_remove_order_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.CharField(blank=True, default='1', max_length=100, null=True),
        ),
    ]
