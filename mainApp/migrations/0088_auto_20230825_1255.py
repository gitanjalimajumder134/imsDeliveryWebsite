# Generated by Django 3.2 on 2023-08-25 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0087_stock_totalquantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='totalquantity',
        ),
        migrations.CreateModel(
            name='HubBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stocktype', models.CharField(blank=True, default='', max_length=100, verbose_name='Type')),
                ('closingstock', models.CharField(blank=True, default='', max_length=100, verbose_name='Closing Stock')),
                ('hubid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='HubBalanceId', to='mainApp.hub', verbose_name='Name')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hubItemId', to='mainApp.product', verbose_name='Item')),
            ],
        ),
    ]