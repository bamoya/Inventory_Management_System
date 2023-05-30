from django.shortcuts import render, redirect
from .forms import CreateUserForm, UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# # Create your views here.



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return redirect('dashboard:index')  # Replace 'index' with your desired URL name
        else:
            return render(request, 'user/log/login.html', {'error_message': 'Invalid login credentials.'})
    else:
        return render(request, 'user/log/login.html')

def logout_user(request):
    logout(request)
    messages.success(request,("You Were Logged Out!"))
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Replace 'home' with your desired URL name
    else:
        form = CreateUserForm()
    return render(request, 'user/log/register.html', {'form': form})


def profile(request):
    return render(request, 'user/profile.html')


def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
    else :
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm( instance=request.user.profile)

    context = {
        'user_form':user_form,
        'profile_form': profile_form,
    }
    return render(request, 'user/profile.html',context)