from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm, ProductForm, SupplierForm, CustomerForm, PurchaseOrderForm, PurchaseOrderItemForm

# Create your views here.

@login_required
def index(request):
    return render(request,'dashboard/admin/admin.html')


@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:addcategory')  
    else:
        form = CategoryForm()
    return render(request, 'dashboard/admin/addcategory.html', {'form': form})




@login_required
def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:addsupplier')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = SupplierForm()
    return render(request, 'dashboard/admin/addsupplier.html', {'form': form})




@login_required
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:addcustomer')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = CustomerForm()
    return render(request, 'dashboard/admin/addcustomer.html', {'form': form})




@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:addproduct')  # Replace 'product_list' with the URL name of the product list view
    else:
        form = ProductForm()
    
    return render(request, 'dashboard/admin/addproduct.html', {'form': form})



@login_required
def add_purchase_order(request):

    if request.method == 'POST':
        purchase_order_form = PurchaseOrderForm(request.POST)
        purchase_order_item_form = PurchaseOrderItemForm(request.POST)
        
        if purchase_order_form.is_valid() and purchase_order_item_form.is_valid():
            purchase_order = purchase_order_form.save()  # Save the purchase order object
            
            purchase_order_item = purchase_order_item_form.save(commit=False)
            purchase_order_item.purchase_order = purchase_order
            purchase_order_item.save()  # Save the purchase order item object
            
            return redirect('dashboard:addpurchase')  # Replace 'purchase_order_list' with the URL name of the purchase order list view
    else:
        purchase_order_form = PurchaseOrderForm()
        purchase_order_item_form = PurchaseOrderItemForm()
    
    return render(request, 'dashboard/staff/addpurchase.html', {
        'purchase_order_form': purchase_order_form,
        'purchase_order_item_form': purchase_order_item_form
    })