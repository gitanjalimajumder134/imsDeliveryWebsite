# Generated by Django 3.2 on 2023-07-26 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0078_auto_20230726_1653'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='supplier_name',
        ),
        migrations.AddField(
            model_name='order',
            name='supplierName',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Supplier'),
        ),
    ]