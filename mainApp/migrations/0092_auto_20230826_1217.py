# Generated by Django 3.2 on 2023-08-26 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0091_hubbalance_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hubbalance',
            name='stocktype',
        ),
        migrations.AlterField(
            model_name='hubbalance',
            name='created_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
