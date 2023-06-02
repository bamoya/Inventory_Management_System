from django.shortcuts import render, redirect
from django.contrib import messages
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm, ProductForm, SupplierForm, CustomerForm, PurchaseOrderForm, PurchaseOrderItemForm, SaleForm, SaleItemForm
from .models import Product, Supplier, PurchaseOrder, PurchaseOrderItem, Customer, Sale, SaleItem, Category
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
        )
        # Add the purchase items

        for key, value in request.POST.items():
            if key.startswith('id_') and value == 'on':
                # The item was selected, so extract the ID and quantity
            
                product_id = key.split('_')[1]
                quantity = int(request.POST.get(f'quantity_{product_id}', 1))
                # price = float(request.POST.get(f'price_{product_id}', 0))
               

                product = Product.objects.get(id=product_id)
                purchase_item = PurchaseOrderItem.objects.create(
                    purchase_order=purchase,
                    product=product,
                    quantity=quantity,
                )
                purchase_item.save()


        # Update the total cost of the purchase
  
        purchase.save()

        # Redirect to the purchase list page
        return redirect('dashboard:purchaselist')
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


@login_required
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
            payment_status = payment_status
        )
        # Add the purchase items


        for key, value in request.POST.items():
            if key.startswith('id_') and value == 'on':
                # The item was selected, so extract the ID and quantity
            
                product_id = key.split('_')[1]
                quantity = int(request.POST.get(f'quantity_{product_id}', 1))
                sale_date = int(request.POST.get(f'quantity_{product_id}', 1))
                payment_status = int(request.POST.get(f'quantity_{product_id}', 1))
                product = Product.objects.get(id=product_id)

                sale_item = SaleItem.objects.create(
                    product=product,
                    sale = sale,
                    quantity=quantity,

                )
                sale_item.save()


        # Update the total cost of the purchase
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
        

# ----------------------- product views ---------------------------

def productlist(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'products' : products,
        'categories' : categories,
    }
    return render(request,'dashboard/staff/productlist.html', context)


def productdetails(request, pk):
    product = Product.objects.get(id=pk)
    context = {
        'product' : product,
    }
    return render(request,'dashboard/staff/productdetails.html', context)

def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard:productlist')
    return render(request, 'dashboard/staff/deleteproduct.html')


def edit_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard:productlist')
        else : print('form not valid')
    else :
        form = ProductForm(instance=product)
    context = {
        'form' : form,
    }

    return render(request,'dashboard/staff/editproduct.html', context)

# ----------------------- category views ---------------------------

def category_list(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories,
    }
    return render(request,'dashboard/staff/categorylist.html',context= context)


def category_details(request, pk):
    category = Category.objects.get(id=pk)
    context = {
        'category' : category,
    }
    return render(request,'dashboard/staff/categorydetails.html', context)

def delete_category(request, pk):
    category = Category.objects.get(id=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('dashboard:categorylist')
    return render(request, 'dashboard/staff/deletecategory.html')


def edit_category(request, pk):
    category = Category.objects.get(id=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('dashboard:categorylist')
        else : print('form not valid')
    else :
        form = ProductForm(instance=category)
    context = {
        'form' : form,
    }

    return render(request,'dashboard/staff/editcategory.html', context)



# -------------------Sale View---------------------------

def sale_list(request):
    sales = Sale.objects.all()
    context = {
        'sales' : sales,

    }
    return render(request,'dashboard/sale/salelist.html', context)

def sale_details(request, pk):
    sale = Sale.objects.get(id=pk)
    sale_items = SaleItem.objects.filter(sale=sale)
    context = {
        'sale' : sale,
        'items' : sale_items,
    }
    return render(request,'dashboard/sale/saledetails.html', context)

def delete_sale(request, pk):
    sale = Sale.objects.get(id=pk)
    if request.method == 'POST':
        sale.delete()
        return redirect('dashboard:salelist')
    return render(request, 'dashboard/sale/deletesale.html')

SaleItemFormSet = modelformset_factory(SaleItem, fields=('product', 'quantity'))


def edit_sale(request, pk):
    sale = Sale.objects.get(id=pk)
    items = SaleItem.objects.filter(sale=sale) 
    if request.method == 'POST':
        sale_form = SaleForm(request.POST, instance=sale)
        for item in items :
            form_item =  SaleItemForm(request.POST, instance=item)
            if form_item.is_valid():
                form_item.save()
            else : 
                print('form 1 not valid')

        if sale_form.is_valid():
            sale_form.save()
            return redirect('dashboard:salelist')
        else : print('form 2 not valid')
    else :
        sale_form = SaleForm(instance=sale)
        item_form = SaleItemFormSet(queryset=items)
    context = {
        'sale_form' : sale_form,
        'item_form' : item_form,
    }
    print('--------------------------------------------------',item_form)
    return render(request,'dashboard/sale/editsale.html', context)



# --------------------Purchase Views---------------------------------------

def purchase_list(request):
    purchases = PurchaseOrder.objects.all()
    context = {
        'purchases' : purchases,

    }
    return render(request,'dashboard/purchase/purchaselist.html', context)

def purchase_details(request, pk):
    purchase = PurchaseOrder.objects.get(id=pk)
    purchase_items = PurchaseOrderItem.objects.filter(purchase_order=purchase)
    context = {
        'purchase' : purchase,
        'items' : purchase_items,
    }
    return render(request,'dashboard/purchase/purchasedetails.html', context)

def delete_purchase(request, pk):
    purchase = PurchaseOrder.objects.get(id=pk)
    if request.method == 'POST':
        purchase.delete()
        return redirect('dashboard:purchaselist')
    return render(request, 'dashboard/purchase/deletepurchase.html')



# -------------------------------- Customer View ---------------------------

def customer_list(request):
    customers = Customer.objects.all()
    context = {
        'customers' : customers,

    }
    return render(request,'dashboard/people/customerlist.html', context)

def customer_details(request, pk):
    customer = Customer.objects.get(id=pk)
    context = {
        'customer' : customer,
    }
    return render(request,'dashboard/people/customerdetails.html', context)

def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('dashboard:customerlist')
    return render(request, 'dashboard/people/deletecustomer.html')


# -------------------------------- Customer View ---------------------------

def supplier_list(request):
    suppliers = Supplier.objects.all()
    context = {
        'suppliers' : suppliers,

    }
    return render(request,'dashboard/people/supplierlist.html', context)

def supplier_details(request, pk):
    supplier = Supplier.objects.get(id=pk)
    context = {
        'supplier' : supplier,
    }
    return render(request,'dashboard/people/supplierdetails.html', context)

def delete_supplier(request, pk):
    supplier = Supplier.objects.get(id=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('dashboard:supplierlist')
    return render(request, 'dashboard/people/deletesupplier.html')