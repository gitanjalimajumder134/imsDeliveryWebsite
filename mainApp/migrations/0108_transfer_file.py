# Generated by Django 3.2 on 2023-11-21 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0107_requisition_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfer',
            name='file',
            field=models.FileField(blank=True, default='', upload_to='', verbose_name='File'),
        ),
    ]
