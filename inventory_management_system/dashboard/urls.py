from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('',views.index, name='index'),
    path('admin/addcategory/', views.add_category, name='addcategory'),
    path('admin/addsupplier/', views.add_supplier, name='addsupplier'),
    path('admin/addcustomer/', views.add_customer, name='addcustomer'),
    path('admin/addproduct/', views.add_product, name='addproduct'),
    path('purchase/addpurchase/', views.add_purchase, name='addpurchase'),
    path('purchase/addsale/', views.add_sale, name='addsale'),
    path('product/productlist/', views.productlist, name='productlist'),
    path('product/productdetails/<int:pk>', views.productdetails, name='productdetails'),
    path('product/deleteproduct/<int:pk>', views.delete_product, name='deleteproduct'),
    path('product/editproduct/<int:pk>', views.edit_product, name='editproduct'),


    path('category/categorylist/', views.category_list, name='categorylist'),
    path('category/categorydetails/<int:pk>', views.category_details, name='categorydetails'),
    path('category/deletecategory/<int:pk>', views.delete_category, name='deletecategory'),
    path('category/editcategory/<int:pk>', views.edit_category, name='editcategory'),

# -----------------sale urls ---------------------------------
    path('sale/salelist/', views.sale_list, name='salelist'),
    path('sale/saledetails/<int:pk>', views.sale_details, name='saledetails'),
    path('sale/deletesale/<int:pk>', views.delete_sale, name='deletesale'),
    path('sale/editsale/<int:pk>', views.edit_sale, name='editsale'),


# -----------------purchase urls ---------------------------------
    path('purchase/purchaselist/', views.purchase_list, name='purchaselist'),
    path('purchase/purchasedetails/<int:pk>', views.purchase_details, name='purchasedetails'),
    path('purchase/deletepurchase/<int:pk>', views.delete_purchase, name='deletepurchase'),

# -----------------customer urls ---------------------------------
    path('customer/customerlist/', views.customer_list, name='customerlist'),
    path('customer/customerdetails/<int:pk>', views.customer_details, name='customerdetails'),
    path('customer/deletecustomer/<int:pk>', views.delete_customer, name='deletecustomer'),
# -----------------customer urls ---------------------------------
    path('supplier/supplierlist/', views.supplier_list, name='supplierlist'),
    path('supplier/supplierdetails/<int:pk>', views.supplier_details, name='supplierdetails'),
    path('supplier/deletesupplier/<int:pk>', views.delete_supplier, name='deletesupplier'),


]
