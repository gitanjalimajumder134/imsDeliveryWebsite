# Generated by Django 3.2 on 2023-09-08 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0093_stock_allids'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='file',
            field=models.FileField(blank=True, default='', upload_to=''),
        ),
    ]