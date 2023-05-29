from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('',views.index, name='index'),
    path('staff/', views.staff, name='staff'),
    path('product/',views.product, name='product'),
    path('order/', views.order, name='order'),
]
