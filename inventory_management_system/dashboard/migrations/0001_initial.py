# Generated by Django 4.2.1 on 2023-05-30 12:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('description', models.TextField(null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('quantity', models.PositiveIntegerField(null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.category')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=100, null=True)),
                ('order_date', models.DateField(auto_now=True)),
                ('status', models.CharField(max_length=100, null=True)),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=100, null=True)),
                ('sale_date', models.DateField(auto_now=True, null=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('payment_status', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(null=True)),
                ('date_updated', models.DateField(auto_now=True, null=True)),
                ('product', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.product')),
            ],
        ),
        migrations.CreateModel(
            name='SaleItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(null=True)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.product')),
                ('sale', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.sale')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(null=True)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.product')),
                ('purchase_order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.purchaseorder')),
            ],
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.supplier'),
        ),
        migrations.AddField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.supplier'),
        ),
    ]
