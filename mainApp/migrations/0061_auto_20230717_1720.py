# Generated by Django 3.2 on 2023-07-17 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0060_alter_transit_receiveddate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='BranchID',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='disbursementDate',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='disbursementStatus',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='orderDate',
        ),
        migrations.AddField(
            model_name='stock',
            name='hubname',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hubid', to='mainApp.hub', verbose_name='Name'),
        ),
        migrations.AddField(
            model_name='stock',
            name='stockfrom',
            field=models.CharField(blank=True, default='', max_length=201, verbose_name='From'),
        ),
        migrations.AddField(
            model_name='stock',
            name='stockto',
            field=models.CharField(blank=True, default='', max_length=201, verbose_name='To'),
        ),
        migrations.AddField(
            model_name='stock',
            name='stocktype',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='type'),
        ),
        migrations.AddField(
            model_name='stock',
            name='suppliername',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supplierid', to='mainApp.supplier', verbose_name='Name'),
        ),
    ]
