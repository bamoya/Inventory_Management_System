"""
URL configuration for inventory_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from user import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/',include('dashboard.urls')),
    path('register/',user_views.register,name="register"),
    path('', auth_views.LoginView.as_view(template_name='user/log/login.html'), name='login'),
    path('logout/', user_views.logout_user, name='logout'),
    path('profile/',user_views.profile_update,name="profile"),
    path('users/userslist',user_views.user_list,name="userlist"),
    path('users/adduser',user_views.add_user,name="adduser"),
    path('users/deleteuser/<int:pk>',user_views.delete_user,name="deleteuser"),
    path('users/edit/<int:pk>',user_views.edit_user,name="edituser"),

] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT )

