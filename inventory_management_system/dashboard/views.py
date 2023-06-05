from django.shortcuts import render, redirect
from django.contrib import messages
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CategoryForm, CreateProductForm,EditProductForm, StockForm ,SupplierForm, CustomerForm, PurchaseOrderForm, PurchaseOrderItemForm, SaleForm, SaleItemForm
from .models import Product, Supplier, PurchaseOrder, PurchaseOrderItem, Customer, Sale, SaleItem, Category, Stock
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth,ExtractYear
from django.db.models.functions import TruncMonth, TruncYear
from django.http import JsonResponse
from datetime import datetime
# Create your views here.


@login_required
def index(request):
    if request.user.is_superuser :
        return index_admin(request)
    elif request.user.groups.filter(name='vendors').exists() :
        return index_vendor(request)
    elif  request.user.groups.filter(name='buyers').exists() :
        return index_buyer(request)

@login_required
@user_passes_test(lambda u:  u.is_superuser, login_url='login')
def index_admin(request):
    products = Product.objects.order_by('-id')[:5]
    suppliers = Supplier.objects.all().count()
    customers = Customer.objects.all().count()
    total_purchases = PurchaseOrder.objects.aggregate(Sum('total_order_cost'))['total_order_cost__sum'] or 0
    total_sales = Sale.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    purchases_received = PurchaseOrder.objects.filter(status = 'received').count()
    purchases_pending = PurchaseOrder.objects.filter(status = 'pending').count()
    sales_paid = Sale.objects.filter(payment_status = 'paid').count()
    sales_unpaid = Sale.objects.filter(payment_status = 'unpaid').count()
    years = Sale.objects.dates('sale_date', 'year')


    if request.method == 'POST':
        selected_year = request.POST.get('year')
        sales = Sale.objects.filter(sale_date__year=selected_year).annotate(
            year=TruncYear('sale_date'),
            month=TruncMonth('sale_date')
        ).values('year', 'month').annotate(
            total_amount=Sum('total_amount')
        ).order_by('year', 'month')
        purchases = PurchaseOrder.objects.filter(order_date__year=selected_year).annotate(
            year=TruncYear('order_date'),
            month=TruncMonth('order_date')
        ).values('year', 'month').annotate(
            total_order_cost=Sum('total_order_cost')
        ).order_by('year', 'month')
        context ={
        'suppliers' : suppliers,
        'customers': customers,
        'products' : products,
        'sales_paid':sales_paid,
        'purchases_received':purchases_received,
        'total_purchases' : total_purchases,
        'total_sales' : total_sales,
        'sales': sales,
        'purchases': purchases,
        'years' : years,
        } 

    else : 
        context ={
            'suppliers' : suppliers,
            'customers': customers,
            'products' : products,
            'sales_paid':sales_paid,
            'sales_unpaid':sales_unpaid,
            'purchases_received':purchases_received,
            'purchases_pending' : purchases_pending,
            'total_purchases' : total_purchases,
            'total_sales' : total_sales,
            'years' : years,
            
        } 
    return render(request,'dashboard/admin/index.html',context=context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='vendors').exists(), login_url='login')
def index_vendor(request):
    products = Product.objects.order_by('-id')[:5]
    customers = Customer.objects.all().count()
    sales_paid = Sale.objects.filter(payment_status = 'paid').count()
    sales_unpaid = Sale.objects.filter(payment_status = 'unpaid').count()
    years = Sale.objects.dates('sale_date', 'year')

    if request.method == 'POST':
        selected_year = request.POST.get('year')
        sales = Sale.objects.filter(sale_date__year=selected_year).annotate(
            year=TruncYear('sale_date'),
            month=TruncMonth('sale_date')
        ).values('year', 'month').annotate(
            total_amount=Sum('total_amount')
        ).order_by('year', 'month')
        context = {
        'customers' : customers,
        'sales_paid' : sales_paid,
        'sales_unpaid' : sales_unpaid,
        'sales' : sales,
        'years' : years,
        'products' :products}
        return render(request,'dashboard/staff/index_vendor.html', context=context)
    else :
        context = {
            'customers' : customers,
            'sales_paid' : sales_paid,
            'sales_unpaid' : sales_unpaid,
            'years' : years,
            'products':products,
        }
    return render(request,'dashboard/staff/index_vendor.html', context=context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='buyers').exists(), login_url='login')
def index_buyer(request):
    products = Product.objects.order_by('-id')[:5]
    suppliers = Supplier.objects.all().count()
    purchases_received = PurchaseOrder.objects.filter(status = 'received').count()
    purchases_pending = PurchaseOrder.objects.filter(status = 'pending').count()
    years = Sale.objects.dates('sale_date', 'year')

    if request.method == 'POST':
        selected_year = request.POST.get('year')
        purchases = PurchaseOrder.objects.filter(order_date__year=selected_year).annotate(
            year=TruncYear('order_date'),
            month=TruncMonth('order_date')
        ).values('year', 'month').annotate(
            total_order_cost=Sum('total_order_cost')
        ).order_by('year', 'month')
        context = {
        'suppliers' : suppliers,
        'purchases_received' : purchases_received,
        'purchases_pending' : purchases_pending,
        'purchases' : purchases,
        'years' : years,
        'products' :products}
        return render(request,'dashboard/staff/index_buyer.html', context=context)
    else :
        context = {
            'suppliers' : suppliers,
            'purchases_received' : purchases_received,
            'purchases_pending' : purchases_pending,
            'years' : years,
            'products':products,
        }
    return render(request,'dashboard/staff/index_buyer.html', context=context)

#--------------------category views----------------------------------------------------------

@login_required
@user_passes_test(lambda u: u.groups.filter(name='buyers').exists() or u.is_superuser, login_url='login')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:categorylist')  
    else:
        form = CategoryForm()
    return render(request, 'dashboard/admin/addcategory.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='buyers').exists() or u.groups.filter(name='vendors').exists() or u.is_superuser, login_url='login')
def category_list(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories,
    }
    return render(request,'dashboard/staff/categorylist.html',context= context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='buyers').exists() or u.groups.filter(name='vendors').exists() or u.is_superuser, login_url='login')
def category_details(request, pk):
    category = Category.objects.get(id=pk)
    context = {
        'category' : category,
    }
    return render(request,'dashboard/staff/categorydetails.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='buyers').exists() or u.is_superuser, login_url='login')
def delete_category(request, pk):
    category = Category.objects.get(id=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('dashboard:categorylist')
    return render(request, 'dashboard/staff/deletecategory.html')


@login_required
@user_passes_test(lambda u: u.groups.filter(name='buyers').exists() or u.is_superuser, login_url='login')
def edit_category(request, pk):
    category = Category.objects.get(id=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('dashboard:categorylist')
        else : return
    else :
        form = EditProductForm(instance=category)
    context = {
        'form' : form,
    }

    return render(request,'dashboard/staff/editcategory.html', context)


#--------------------product views----------------------------------------------------------

@login_required
@user_passes_test(lambda u: u.groups.filter(name='buyers').exists() or u.is_superuser, login_url='login')
@login_required
def add_product(request):
    if request.method == 'POST':
        form = CreateProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:productlist')  
    else:
        form = CreateProductForm()
    
    return render(request, 'dashboard/admin/addproduct.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='buyers').exists() or u.groups.filter(name='vendors').exists() or u.is_superuser, login_url='login')
def productlist(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'products' : products,
        'categories' : categories,
    }
    return render(request,'dashboard/staff/productlist.html', context)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='buyers').exists() or u.groups.filter(name='vendors').exists() or u.is_superuser, login_url='login')
def productdetails(request, pk):
    product = Product.objects.get(id=pk)
    context = {
        'product' : product,
    }
    return render(request,'dashboard/staff/productdetails.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='buyers').exists() or u.is_superuser, login_url='login')
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard:productlist')
    return render(request, 'dashboard/staff/deleteproduct.html')


@login_required
@user_passes_test(lambda u: u.groups.filter(name='buyers').exists() or u.is_superuser, login_url='login')
def edit_product(request, pk):
    product = Product.objects.get(id=pk)
    stock = product.stock
    if request.method == 'POST':
        form = EditProductForm(request.POST, instance=product)
        stock_form = StockForm(request.POST,instance=stock)
        if form.is_valid() and stock_form.is_valid():
            form.save()
            stock_form.save()
            return redirect('dashboard:productlist')
        else : return
    else :
        form = EditProductForm(instance=product)
        stock_form = StockForm(instance=stock)
    context = {
        'form' : form,
        'stock_form' : stock_form,
    }

    return render(request,'dashboard/staff/editproduct.html', context)

#--------------------Customer views----------------------------------------------------------


@login_required
@user_passes_test(lambda u: u.groups.filter(name='vendors').exists() or u.is_superuser, login_url='login')
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
@user_passes_test(lambda u: u.groups.filter(name='vendors').exists() or u.is_superuser, login_url='login')
def customer_list(request):
    customers = Customer.objects.all()
    context = {
        'customers' : customers,

    }
    return render(request,'dashboard/people/customerlist.html', context)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='vendors').exists() or u.is_superuser, login_url='login')
def customer_details(request, pk):
    customer = Customer.objects.get(id=pk)
    context = {
        'customer' : customer,
    }
    return render(request,'dashboard/people/customerdetails.html', context)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='vendors').exists() or u.is_superuser, login_url='login')
def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('dashboard:customerlist')
    return render(request, 'dashboard/people/deletecustomer.html')


#--------------------Supplier views----------------------------------------------------------


@login_required
@user_passes_test(lambda u: u.groups.filter(name='buyers').exists() or u.is_superuser, login_url='login')
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
@user_passes_test(lambda u: u.groups.filter(name='buyers').exists() or u.is_superuser, login_url='login')
def supplier_list(request):
    suppliers = Supplier.objects.all()
    context = {
        'suppliers' : suppliers,

    }
    return render(request,'dashboard/people/supplierlist.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='buyers').exists() or u.is_superuser, login_url='login')
def supplier_details(request, pk):
    supplier = Supplier.objects.get(id=pk)
    context = {
        'supplier' : supplier,
    }
    return render(request,'dashboard/people/supplierdetails.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='buyers').exists() or u.is_superuser, login_url='login')
def delete_supplier(request, pk):
    supplier = Supplier.objects.get(id=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('dashboard:supplierlist')
    return render(request, 'dashboard/people/deletesupplier.html')




#--------------------Purchase views----------------------------------------------------------



@login_required
@user_passes_test(lambda u: u.groups.filter(name='buyers').exists() or u.is_superuser, login_url='login')
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

                new_quantity = product.stock.quantity + quantity
                if new_quantity > product.max_quantity:
                    message = f'Oops! You passed the Max Qty for product {product.name} product'

                    return render(request, 'partials/error.html',{'message' : message,})
                else : 
                    stock = Stock.objects.get(product=product)
                    stock.quantity = new_quantity
                    stock.save()
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
@user_passes_test(lambda u: u.groups.filter(name='buyers').exists() or u.is_superuser, login_url='login')
def purchase_list(request):
    purchases = PurchaseOrder.objects.all()
    context = {
        'purchases' : purchases,

    }
    return render(request,'dashboard/purchase/purchaselist.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='buyers').exists() or u.is_superuser, login_url='login')
def purchase_details(request, pk):
    purchase = PurchaseOrder.objects.get(id=pk)
    purchase_items = PurchaseOrderItem.objects.filter(purchase_order=purchase)
    context = {
        'purchase' : purchase,
        'items' : purchase_items,
    }
    return render(request,'dashboard/purchase/purchasedetails.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='buyers').exists() or u.is_superuser, login_url='login')
def delete_purchase(request, pk):
    purchase = PurchaseOrder.objects.get(id=pk)
    if request.method == 'POST':
        purchase.delete()
        return redirect('dashboard:purchaselist')
    return render(request, 'dashboard/purchase/deletepurchase.html')



#--------------------Sale views----------------------------------------------------------


@login_required
@user_passes_test(lambda u: u.groups.filter(name='vendors').exists() or u.is_superuser, login_url='login')
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

                new_quantity = product.stock.quantity - quantity
                if new_quantity < 0 :
                    message = f'Oops! You passed the stock Qty for {product.name} product'

                    return render(request, 'partials/error.html',{'message' : message,})
                
                else :
                    stock = Stock.objects.get(product=product)
                    stock.quantity = new_quantity
                    stock.save()
                    sale_item = SaleItem.objects.create(
                        product=product,
                        sale = sale,
                        quantity=quantity,

                    )
                    sale_item.save()


        # Update the total cost of the purchase
        sale.save()

        # Redirect to the purchase list page
        return redirect('dashboard:salelist')
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
        
@login_required
@user_passes_test(lambda u: u.groups.filter(name='vendors').exists() or u.is_superuser, login_url='login')
def sale_list(request):
    sales = Sale.objects.all()
    context = {
        'sales' : sales,

    }
    return render(request,'dashboard/sale/salelist.html', context)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='vendors').exists() or u.is_superuser, login_url='login')
def sale_details(request, pk):
    sale = Sale.objects.get(id=pk)
    sale_items = SaleItem.objects.filter(sale=sale)
    context = {
        'sale' : sale,
        'items' : sale_items,
    }
    return render(request,'dashboard/sale/saledetails.html', context)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='vendors').exists() or u.is_superuser, login_url='login')
def delete_sale(request, pk):
    sale = Sale.objects.get(id=pk)
    if request.method == 'POST':
        sale.delete()
        return redirect('dashboard:salelist')
    return render(request, 'dashboard/sale/deletesale.html')

SaleItemFormSet = modelformset_factory(SaleItem, fields=('product', 'quantity'))


@login_required
@user_passes_test(lambda u: u.groups.filter(name='vendors').exists() or u.is_superuser, login_url='login')
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
                return

        if sale_form.is_valid():
            sale_form.save()
            return redirect('dashboard:salelist')
        else :
            pass
    else :
        sale_form = SaleForm(instance=sale)
        item_form = SaleItemFormSet(queryset=items)
    context = {
        'sale_form' : sale_form,
        'item_form' : item_form,
    }
    return render(request,'dashboard/sale/editsale.html', context)
#