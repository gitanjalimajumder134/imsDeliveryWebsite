# Generated by Django 3.2 on 2023-09-26 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0097_alter_adjustment_adjustmentdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adjustment',
            name='adjustmentDate',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Adjustment Date'),
        ),
    ]