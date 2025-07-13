from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm

# Home page (public)
def index(request):
    return render(request, 'index.html')

# Dashboard (requires login)
@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user})

# Materials/resources page (requires login)
@login_required
def materials(request):
    return render(request, 'materials.html', {'user': request.user})

# Assignments page (requires login)
@login_required
def assignments(request):
    return render(request, 'assignments.html', {'user': request.user})

# Notifications page (requires login)
@login_required
def notifications(request):
    return render(request, 'notifications.html', {'user': request.user})

# Profile page (requires login)
@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
