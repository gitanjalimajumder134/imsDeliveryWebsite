# Generated by Django 3.2 on 2023-12-12 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0120_alter_order_orderstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfer',
            name='transferdate',
            field=models.DateField(auto_now=True, null=True, verbose_name='Tranfer Date'),
        ),
    ]