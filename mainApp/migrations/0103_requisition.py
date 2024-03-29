# Generated by Django 3.2 on 2023-11-20 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0102_auto_20231116_1139'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requisition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requisitionNumber', models.CharField(blank=True, default='', max_length=100, verbose_name='Requisition Number')),
                ('status', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], db_column='Status', default='InTransit', max_length=100)),
                ('requisitionDate', models.DateField(auto_now_add=True, null=True, verbose_name='Requisition Date')),
                ('branchName', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='branch', to='mainApp.branch', verbose_name='Branch')),
                ('hubName', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hubName', to='mainApp.hub', verbose_name='Hub')),
                ('productname', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='productname', to='mainApp.product', verbose_name='Items')),
            ],
            options={
                'verbose_name': 'Requisition',
                'ordering': ('-id',),
            },
        ),
    ]
