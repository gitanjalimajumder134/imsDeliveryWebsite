# Generated by Django 3.2 on 2022-10-31 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0013_auto_20221029_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='disbursementStatus',
            field=models.CharField(choices=[('disbursed', 'Disbursed'), ('not_disbursed', 'Not Disbursed')], default='not_disbursed', max_length=100),
        ),
        migrations.AlterField(
            model_name='stock',
            name='stockStatus',
            field=models.CharField(blank=True, choices=[('pending', 'Pending'), ('delivered', 'Delivered')], default='pending', max_length=100),
        ),
    ]