from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100,null=True)
    email = models.EmailField(null=True) 
    phone = models.CharField(max_length=20,null=True)
    address = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100,null=True)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    quantity = models.PositiveIntegerField( null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL,null=True)
    # poduct_image = models.ImageField(upload_to='product_images',null=True)

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    order_number = models.CharField(max_length=100, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    staff = models.ForeignKey(User,on_delete= models.SET_NULL, null=True)
    order_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.order_number

class PurchaseOrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)
    date_updated = models.DateField(auto_now=True, null=True)

    def __str__(self):
        return f'{self.product} - {self.quantity}'

class Sale(models.Model):
    customer = models.CharField(max_length=100, null=True)
    sale_date = models.DateField(auto_now=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payment_status = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.customer} - {self.total_amount}'

class SaleItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField( null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
