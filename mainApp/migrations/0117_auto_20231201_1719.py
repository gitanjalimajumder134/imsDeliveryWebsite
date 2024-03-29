# Generated by Django 3.2 on 2023-12-01 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0116_auto_20231125_1239'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='gst',
            new_name='cgst',
        ),
        migrations.AddField(
            model_name='product',
            name='igst',
            field=models.CharField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='product',
            name='sgst',
            field=models.CharField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='product',
            name='cgst',
            field=models.CharField(blank=True, db_column='gst', max_length=254),
        ),
    ]
