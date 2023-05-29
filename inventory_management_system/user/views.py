from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse

# # Create your views here.



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return redirect('dashboard:index')  # Replace 'index' with your desired URL name
        else:
            return render(request, 'user/login.html', {'error_message': 'Invalid login credentials.'})
    else:
        return render(request, 'user/login.html')


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:index')  # Replace 'home' with your desired URL name
    else:
        form = CreateUserForm()
    return render(request, 'user/register.html', {'form': form})


