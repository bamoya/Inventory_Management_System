from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile

class CreateUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta :
        model = User
        fields = ['first_name','last_name' ,'username','email','password1','password2']



class UserUpdateForm(UserChangeForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['adress','phone','image']