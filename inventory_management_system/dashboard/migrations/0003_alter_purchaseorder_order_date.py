# Generated by Django 4.2.1 on 2023-05-30 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_customer_sale_sale_number_sale_staff_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='order_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
