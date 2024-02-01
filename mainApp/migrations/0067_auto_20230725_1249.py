# Generated by Django 3.2 on 2023-07-25 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0066_transferquantity_transfer'),
    ]

    operations = [
        migrations.AddField(
            model_name='transferquantity',
            name='hub',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hublist', to='mainApp.hub'),
        ),
        migrations.AlterField(
            model_name='transferquantity',
            name='comment',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='transferquantity',
            name='stocktransfered',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Stock to be Transfered'),
        ),
        migrations.AlterField(
            model_name='transferquantity',
            name='transferablestock',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Transferable Stock'),
        ),
    ]
