# Generated by Django 3.2 on 2023-07-25 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0072_auto_20230725_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='receiveddate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Transfer Date'),
        ),
    ]
