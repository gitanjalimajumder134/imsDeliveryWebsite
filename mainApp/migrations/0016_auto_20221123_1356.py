# Generated by Django 3.2 on 2022-11-23 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0015_alter_order_orderstatus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='adminUserID',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='stockBranchID',
        ),
        migrations.AlterField(
            model_name='order',
            name='orderStatus',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Delivered', 'Delivered')], default='Pending', max_length=100),
        ),
        migrations.AlterField(
            model_name='stock',
            name='disbursementStatus',
            field=models.CharField(choices=[('Disbursed', 'Disbursed'), ('Notdisbursed', 'Not Disbursed')], default='Notdisbursed', max_length=100),
        ),
        migrations.AlterField(
            model_name='stock',
            name='stockStatus',
            field=models.CharField(blank=True, choices=[('InTransit', 'In Transit'), ('delivered', 'Delivered')], default='InTransit', max_length=100),
        ),
    ]
