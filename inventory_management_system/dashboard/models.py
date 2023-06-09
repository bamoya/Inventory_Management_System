from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
import datetime
from django.db.models import Sum

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name
    

class Customer(models.Model):
    name = models.CharField(max_length=100,null=True)
    email = models.EmailField(null=True) 
    phone = models.CharField(max_length=20,null=True)
    address = models.CharField(max_length=100,null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name
    

class Supplier(models.Model):
    name = models.CharField(max_length=100,null=True)
    email = models.EmailField(null=True) 
    phone = models.CharField(max_length=20,null=True)
    address = models.CharField(max_length=100,null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100,null=True)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE,null=True)
    min_quantity = models.PositiveIntegerField(null=True)
    max_quantity = models.PositiveBigIntegerField(null=True)
    def __str__(self):
        return self.name

class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)
    date_updated = models.DateField(auto_now=True, null=True)

    def __str__(self):
        return f'{self.product} - {self.quantity}'




received_status = [('received','received'),('pending', 'pending')]

class PurchaseOrder(models.Model):
    order_number = models.CharField(unique=True,max_length=100, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    staff = models.ForeignKey(User,on_delete= models.SET_NULL, null=True)
    order_date = models.DateField(default=datetime.date.today,null=True)
    status = models.CharField(max_length=100, null=True,choices=received_status)
    total_order_cost = models.DecimalField(max_digits=10, decimal_places=2,null=True, editable=False)
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = get_random_string(length=10)  # Generate a random string as the order number
        
        self.total_order_cost = PurchaseOrderItem.objects.filter(purchase_order=self).aggregate(Sum('total_price'))['total_price__sum'] or 0
        super().save(*args, **kwargs)
        

    def __str__(self):
        return f'{self.supplier} - {self.total_order_cost}'

class PurchaseOrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)
    # unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, editable=False)

    def __str__(self):
        return f'{self.product} - {self.total_price}'
    
    def save(self, *args, **kwargs):
        # calculate total_price 
        self.total_price = self.product.price*self.quantity 
        super().save(*args, **kwargs)








payment_status = [('paid','paid'),('unpaid', 'unpaid')]
class Sale(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True)
    sale_number = models.CharField(unique=True,max_length=100, null=True)
    staff = models.ForeignKey(User,on_delete= models.SET_NULL, null=True)
    sale_date = models.DateField(default=datetime.date.today, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, editable=False)
    payment_status = models.CharField(max_length=100, null=True,choices=payment_status)

    def save(self, *args, **kwargs):
        if not self.sale_number:
            self.sale_number = get_random_string(length=10)  # Generate a random string as the sale number

        # calculate total_amount based on related SaleItem objects
        self.total_amount = SaleItem.objects.filter(sale=self).aggregate(Sum('total_price'))['total_price__sum'] or 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.customer} - {self.total_amount}'
    



class SaleItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField( null=True)
    # unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, editable=False)

    def __str__(self):
        return f'{self.product} - {self.total_price}'

    def save(self, *args, **kwargs):

        # calculate total_price 
        self.total_price = self.product.price*self.quantity 
        super().save(*args, **kwargs)
