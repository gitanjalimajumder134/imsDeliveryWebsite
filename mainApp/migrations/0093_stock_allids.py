# Generated by Django 3.2 on 2023-08-28 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0092_auto_20230826_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='allids',
            field=models.CharField(blank=True, max_length=201, null=True),
        ),
    ]