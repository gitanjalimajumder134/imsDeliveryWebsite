# Generated by Django 3.2 on 2023-12-28 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0124_alter_transit_transitdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transit',
            name='transitdate',
            field=models.DateField(db_column='Po_date', verbose_name='Po Date'),
        ),
    ]
