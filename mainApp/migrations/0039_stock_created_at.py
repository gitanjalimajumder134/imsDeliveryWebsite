# Generated by Django 3.2 on 2023-01-31 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0038_product_hsn'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
