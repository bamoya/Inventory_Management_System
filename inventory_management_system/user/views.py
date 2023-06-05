from django.shortcuts import render, redirect
from .forms import CreateUserForm, UserUpdateForm,ProfileUpdateForm, AddUserForm, EditUserForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile
# from django.forms import 

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



def user_list(request):
    users = User.objects.all()
    context = {
        'users' : users,

    }
    return render(request,'user/userlist.html', context)

def add_user(request):
    if request.method == 'POST':
            form = AddUserForm(request.POST)
            profile_form = ProfileUpdateForm(request.POST)
            if form.is_valid() and profile_form.is_valid() :
                form.save()
                
                return redirect('userlist')  # Replace 'home' with your desired URL name
    else:
        profile_form = ProfileUpdateForm()
        form = AddUserForm()
    context ={
        'form' : form,
        'profile_form' : profile_form,
    }
    return render(request, 'user/adduser.html', context=context)


def edit_user(request,pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
            user_form = EditUserForm(request.POST,instance = user)
            profile_form = ProfileUpdateForm(request.POST,instance=user.profile)
            grp_name = request.POST['grp']
            if grp_name != 'none' :
                group = Group.objects.get(name=grp_name)
            # password_form = PasswordChangeForm( user ,request.POST)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                if grp_name != 'none':
                    user.groups.add(group)
                profile_form.save()
                # password_form.save(commit=False)
                return redirect('userlist')  # Replace 'home' with your desired URL name
    else:
        user_form = EditUserForm(instance = user)
        profile_form = ProfileUpdateForm(instance=user.profile)
        # password_form = PasswordChangeForm(user)
    context= {
        'user_form' : user_form,
        'profile_form': profile_form
        # 'password_form':password_form,
    }
    return render(request, 'user/edituser.html',context=context)



def delete_user(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('userlist')
    return render(request, 'user/deleteuser.html')