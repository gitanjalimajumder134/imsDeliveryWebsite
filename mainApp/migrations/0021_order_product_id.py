# Generated by Django 3.2 on 2022-11-23 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0020_auto_20221123_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.product'),
        ),
    ]
