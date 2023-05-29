from django.db import models
from django.contrib.auth.models import User
# Create your models here.

categories = [('Electronics','Electronics'),
              ('Food','Food'),
              ('Accessory','Accessory')]

class Product(models.Model):
    name = models.CharField(max_length=100 , null=True)
    category = models.CharField(max_length=100,choices=categories, null=True)
    quantity = models.PositiveIntegerField(null=True)


    def __str__(self):
        return f'{self.name}'
    
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE , null=True)
    staff = models.ForeignKey(User,models.CASCADE,null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.product} ordered by : {self.staff}'
    


    