from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import (
  UserRegistrationForm,
  LoginForm,
  UserProfileUpdateForm
)

from .decorators import(
  not_logged_in_required
)

from .models import User

@never_cache
@not_logged_in_required
def login_user(request):
  form = LoginForm()
  
  if request.method == "POST":
    form = LoginForm(request.POST)
    if form.is_valid():
      user = authenticate(
        username = form.cleaned_data.get('username'),
        password = form.cleaned_data.get('password')
      )
      if user:
        login(request, user)
        return redirect('home')
      
      else:
        messages.warning(request, "wrong credentials")
  
  
  context = {
    "form": form
  }
  return render(request, 'login.html', context)


def logout_user(request):
  logout(request)
  return redirect('login')


@never_cache
@not_logged_in_required
def register_user(request):
  form = UserRegistrationForm()
  if request.method == "POST":
    form = UserRegistrationForm(request.POST)
    
    if form.is_valid():
      user = form.save(commit=False)
      user.set_password(form.cleaned_data.get('password'))
      user.save()
      messages.success(request, "Registration successful")
      return redirect('login')
    
  context = {
    "form": form
  }
  return render(request, 'registration.html', context)

@login_required(login_url='login')
def profile(request):
  account = get_object_or_404(User, pk=request.user.pk)
  form = UserProfileUpdateForm(instance=account)
  
  if request.method == 'POST':
    if request.user.pk != account.pk:
      return redirect('home')
    
    form = UserProfileUpdateForm(request.POST, instance=account)
    if form.is_valid():
      form.save()
      messages.success(request, "profile has been updated successfully")
      return redirect('profile')
      
    
  context = {
    "account": account,
    "form": form
  }
  return render(request, 'profile.html', context)