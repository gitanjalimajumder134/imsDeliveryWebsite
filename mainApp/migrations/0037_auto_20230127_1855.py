# Generated by Django 3.2 on 2023-01-27 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0036_auto_20230127_1829'),
    ]

    operations = [
        migrations.RenameField(
            model_name='branch',
            old_name='branchMangerNo',
            new_name='branchMangerPhoneNo',
        ),
        migrations.AlterField(
            model_name='branch',
            name='branchMangerPhoneNo',
            field=models.CharField(blank=True, db_column='branchMangerNo', default='', max_length=100),
        ),
    ]
