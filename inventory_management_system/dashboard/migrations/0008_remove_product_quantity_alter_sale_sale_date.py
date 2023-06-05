# Generated by Django 4.2.1 on 2023-06-05 14:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_remove_purchaseorderitem_unit_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
        migrations.AlterField(
            model_name='sale',
            name='sale_date',
            field=models.DateField(default=datetime.date.today, null=True),
        ),
    ]
