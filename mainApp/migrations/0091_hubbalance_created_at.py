# Generated by Django 3.2 on 2023-08-25 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0090_auto_20230825_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='hubbalance',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
