from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    return render(request,'dashboard/admin/admin.html')

@login_required
def staff(request):
    return render(request,'dashboard/staff.html')

@login_required
def product(request):
    return render(request,'dashboard/product.html')

@login_required
def order(request):
    return render(request, 'dashboard/order.html')

