# Generated by Django 3.2 on 2023-08-18 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0084_auto_20230818_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='transferid',
        ),
    ]
