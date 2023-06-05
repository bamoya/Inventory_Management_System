from django import forms
from django.contrib.auth.models import User,Group
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
        fields = ['address','phone','image']

class AddUserForm(UserCreationForm):
    grps = (('vendors','vendors'),('buyers','buyers'))
    is_staff = forms.BooleanField(required=False)
    is_superuser = forms.BooleanField(required=False)
    grp = forms.ChoiceField(choices=grps, required=False)
    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email', 'password1', 'password2', 'is_staff', 'is_superuser','grp')
        widgets  = {
            'email' : forms.TextInput(),
            'grp' : forms.Select(attrs={'class': 'select'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = self.cleaned_data['is_staff']
        user.is_superuser = self.cleaned_data['is_superuser']
        grp_name = self.cleaned_data['grp']
        group = Group.objects.get(name=grp_name)
        if commit:
            user.save()
            user.groups.add(group)
        return user

class EditUserForm(UserChangeForm):
    is_staff = forms.BooleanField(required=False)
    is_superuser = forms.BooleanField(required=False)
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','is_staff','is_superuser')
        widgets  = {
            'email' : forms.TextInput(),
        }
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = self.cleaned_data['is_staff']
        user.is_superuser = self.cleaned_data['is_superuser']
        if commit:
            user.save()
        return user
    

