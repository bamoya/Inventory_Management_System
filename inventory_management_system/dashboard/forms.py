# forms.py
from django import forms
from .models import Category,Product,Supplier, Customer, PurchaseOrder, PurchaseOrderItem,Sale, SaleItem
from django.forms import inlineformset_factory, modelformset_factory


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets  = {
            'category' : forms.Select(attrs={'class': 'select'}),
            'supplier' : forms.Select(attrs={'class': 'select'}),
            'quantity' : forms.TextInput(),
            'price' : forms.TextInput(),
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'



# class PurchaseOrderForm(forms.ModelForm):
#     class Meta:
#         model = PurchaseOrder
#         fields = '__all__'  

# class PurchaseOrderItemForm(forms.ModelForm):
#     class Meta:
#         model = PurchaseOrderItem
#         fields = '__all__'  

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['supplier', 'staff', 'order_date','status']


class PurchaseOrderItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderItem
        fields = ['product', 'quantity']


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'
        widgets  = {
            'customer' : forms.Select(attrs={'class': 'select'}),
            'staff' : forms.Select(attrs={'class': 'select'}),
            'payment_status' : forms.Select(attrs={'class': 'select'}),
        }

class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity']
        widgets  = {
            'product' : forms.Select(attrs={'class': 'select'}),
            'quantity' : forms.TextInput(),
        }
    