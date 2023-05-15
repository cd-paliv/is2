"""OMD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, re_path
from django.views.generic.base import TemplateView
from OMDApp.views.accounts_view import LoginView, LogOut, RegisterView, RegisterDogView, RegisterSingleDogView, ProfileView, EditProfileView, EditPasswordView, AskForTurn
from OMDApp.views.dogs_view import DogListView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    # Accounts
    path('register/', RegisterView, name='register'),
    path('registerdog/<int:owner_id>/', RegisterDogView, name='registerDog'),
    path('registersingledog', RegisterSingleDogView, name='registerSingleDog'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOut, name='logout'),
    path('profile/', ProfileView, name='profile'),
    path('editprofile/', EditProfileView.as_view(), name='editProfile'),
    path('editpassword/', EditPasswordView.as_view(), name='editPassword'),
    path('askforturn/', AskForTurn, name='askForTurn'),
    
    # Dogs
    path('mydogs/', DogListView.as_view(), name='dog_list'),
]
