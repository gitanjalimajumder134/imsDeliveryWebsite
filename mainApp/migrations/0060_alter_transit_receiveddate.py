# Generated by Django 3.2 on 2023-07-17 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0059_alter_transit_receiveddate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transit',
            name='receiveddate',
            field=models.DateField(blank=True, null=True),
        ),
    ]