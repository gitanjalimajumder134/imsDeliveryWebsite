# Generated by Django 3.2 on 2023-07-25 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0073_auto_20230725_1821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='created_at',
        ),
    ]
