# Generated by Django 3.2 on 2023-01-04 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0032_remove_order_loanstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='loanStatus',
            field=models.CharField(choices=[('Active', 'Active'), ('InActive', 'InActive')], default='Active', max_length=100),
        ),
    ]