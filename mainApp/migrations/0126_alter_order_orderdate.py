# Generated by Django 3.2 on 2024-01-11 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0125_alter_transit_transitdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='orderDate',
            field=models.DateField(blank=True, default='', max_length=100, null=True),
        ),
    ]
