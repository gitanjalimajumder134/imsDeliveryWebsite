# Generated by Django 3.2 on 2023-12-01 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0118_order_salehuub'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='salehuub',
        ),
        migrations.AddField(
            model_name='order',
            name='salehub',
            field=models.ForeignKey(blank=True, db_column='salehuub', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Salehub', to='mainApp.hub', verbose_name='Sale Hub'),
        ),
    ]
