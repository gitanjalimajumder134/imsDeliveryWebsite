# Generated by Django 3.2 on 2023-07-18 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0065_transferquantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='transferquantity',
            name='transfer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transferid', to='mainApp.transfer'),
        ),
    ]
