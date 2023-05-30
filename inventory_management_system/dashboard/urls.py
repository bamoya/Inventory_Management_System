from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('',views.index, name='index'),
    path('admin/addcategory/', views.add_category, name='addcategory'),
    path('admin/addsupplier/', views.add_supplier, name='addsupplier'),
    path('admin/addcustomer/', views.add_customer, name='addcustomer'),
    path('admin/addproduct/', views.add_product, name='addproduct'),
    path('addpurchase/', views.add_purchase_order, name='addpurchase'),
]
