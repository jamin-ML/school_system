# Import Django shortcuts for rendering templates, redirecting, and fetching objects or 404
from django.shortcuts import render, redirect, get_object_or_404
# Import decorator to require login for certain views
from django.contrib.auth.decorators import login_required
# Import authentication helpers for login/logout
from django.contrib.auth import authenticate, login, logout
# Import built-in forms for user creation and authentication
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Import custom user creation form
from .forms import CustomUserCreationForm
# Import the Resource model for resource-related views
from .models import Material,Topic,Subject,SubTopic
from bs4 import BeautifulSoup


#---------------------------------------
# Home page view (publicly accessible)
#---------------------------------------

def index(request):
    # Render the index.html template
    return render(request, 'index.html')

#---------------------------------------
# Materials/resources page (requires login)
#---------------------------------------

@login_required
def materials(request):
    materials = Material.objects.all()
    return render(request, 'materials.html', {'materials': materials})

#---------------------------------------
# User login view (handles GET and POST)
#---------------------------------------


def user_login(request):
    if request.method == 'POST':
        # If POST, process the submitted login form
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # If form is valid, log the user in and redirect to dashboard
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        # If GET, display a blank login form
        form = AuthenticationForm()
    # Render the login.html template with the form
    return render(request, 'login.html', {'form': form})

# User logout view
def user_logout(request):
    # Log the user out and redirect to the home page
    logout(request)
    return redirect('index')

#---------------------------------------
# User registration view (handles GET and POST)
#---------------------------------------

def register(request):
    if request.method == 'POST':
        # If POST, process the submitted registration form
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # If form is valid, create the user, log them in, and redirect to dashboard
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        # If GET, display a blank registration form
        form = CustomUserCreationForm()
    # Render the register.html template with the form
    return render(request, 'register.html', {'form': form})

#--------------------------------------
# Material detail view (requires login)
#---------------------------------------

from django.shortcuts import render, get_object_or_404
from .models import Material, Subject # Make sure to import your models
def material_detail(request, pk):
    current_material = get_object_or_404(Material, pk=pk)

    subject = current_material.subtopic.topic.subject

    previous_material = Material.objects.filter(
        subtopic=current_material.subtopic,
        order__lt=current_material.order
    ).order_by('-order').first()

    next_material = Material.objects.filter(
        subtopic=current_material.subtopic,
        order__gt=current_material.order
    ).order_by('order').first()

    context = {
        'subject': subject,
        'current_material': current_material,
        'previous_material': previous_material,
        'next_material': next_material,
        'topic': current_material.subtopic.topic,
    }

    # ✅ This must always be reached!
    return render(request, 'material_detail.html', context)


def dashboard_view(request):
    return render(request, 'dashboard.html')
