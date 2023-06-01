from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm, ProductForm, SupplierForm, CustomerForm, PurchaseOrderForm, PurchaseOrderItemForm, PurchaseOrderItemFormSet
from .models import Product, Supplier, PurchaseOrder, PurchaseOrderItem, Customer, Sale, SaleItem
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

def add_purchase(request):
    if request.method == 'POST':
        # Retrieve the form data
        supplier_name = request.POST.get('supplier')
        purchase_date = request.POST.get('date')
        status = request.POST.get('status')
        staff = request.user

        # Create a new purchase
        supplier = Supplier.objects.get(name=supplier_name)
        purchase = PurchaseOrder.objects.create(
            supplier=supplier,
            staff = staff,
            order_date = purchase_date,
            status = status,
            total_order_cost=0
        )
        # Add the purchase items
        total_order_cost = 0
        for key, value in request.POST.items():
            if key.startswith('id_') and value == 'on':
                # The item was selected, so extract the ID and quantity
            
                product_id = key.split('_')[1]
                quantity = int(request.POST.get(f'quantity_{product_id}', 1))
                price = float(request.POST.get(f'price_{product_id}', 0))
               

                total_price = quantity * price
                product = Product.objects.get(id=product_id)
                purchase_item = PurchaseOrderItem.objects.create(
                    purchase_order=purchase,
                    product=product,
                    quantity=quantity,
                    unit_price=price,
                    total_price= total_price,
                )
                purchase_item.save()
                total_order_cost += total_price

        # Update the total cost of the purchase
        purchase.total_order_cost = total_order_cost
        purchase.save()

        # Redirect to the purchase list page
        return redirect('dashboard:index')
    else:
        # Retrieve the suppliers from the database
        suppliers = Supplier.objects.all()
        status = request.GET.get('status')
        purchase_date = request.GET.get('date')
        # Check if a supplier name was passed in the query parameters
        supplier_id = request.GET.get('supplier')
        # print(supplier_name)
        if supplier_id:
            # Retrieve the selected supplier and products from the database
            supplier = Supplier.objects.get(id=supplier_id)
            products = Product.objects.filter(supplier=supplier)

            context = {
                'supplier': supplier,
                'status':status,
                'date' : purchase_date,
                'products': products
            }

            return render(request, 'dashboard/staff/addpurchase.html', context)
        else:
            context = {
                'suppliers': suppliers
            }


            return render(request, 'dashboard/staff/addpurchase.html', context)



def add_sale(request):
    if request.method == 'POST':
        # Retrieve the form data
        cusomer_name = request.POST.get('customer')
        sale_date = request.POST.get('date')
        payment_status = request.POST.get('status')
        staff = request.user

        # Create a new sale
        customer = Customer.objects.get(name=cusomer_name)
        sale = Sale.objects.create(
            customer=customer,
            staff = staff,
            sale_date = sale_date,
            total_amount=0,
            payment_status = payment_status
        )
        # Add the purchase items

        total_amount = 0
        for key, value in request.POST.items():
            if key.startswith('id_') and value == 'on':
                # The item was selected, so extract the ID and quantity
            
                product_id = key.split('_')[1]
                quantity = int(request.POST.get(f'quantity_{product_id}', 1))
                sale_date = int(request.POST.get(f'quantity_{product_id}', 1))
                payment_status = int(request.POST.get(f'quantity_{product_id}', 1))
                product = Product.objects.get(id=product_id)
                price = product.price
                total_price = quantity * price

                sale_item = SaleItem.objects.create(
                    product=product,
                    sale = sale,
                    quantity=quantity,
                    unit_price=price,
                    total_price= total_price,
                )
                sale_item.save()
                total_amount += total_price

        # Update the total cost of the purchase
        sale.total_amount = total_amount
        sale.save()

        # Redirect to the purchase list page
        return redirect('dashboard:index')
    else:
        # Retrieve the customers from the database
        customers = Customer.objects.all()

        # Check if a customer name was passed in the query parameters
        customer_id = request.GET.get('customer')
        payment_status = request.GET.get('status')
        sale_date = request.GET.get('date')
        # print(supplier_name)
        if customer_id:
            # Retrieve the selected customer and products from the database
            customer = Customer.objects.get(id=customer_id)
            products = Product.objects.all()

            context = {
                'customer': customer,
                'status':payment_status,
                'date' : sale_date,
                'products': products
            }

            return render(request, 'dashboard/staff/addsale.html', context)
        else:
            context = {
                'customers': customers
            }


            return render(request, 'dashboard/staff/addsale.html', context)