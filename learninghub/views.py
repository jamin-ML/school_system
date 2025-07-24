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
from .models import Resource,Material


# Home page view (publicly accessible)
def index(request):
    # Render the index.html template
    return render(request, 'index.html')

# Dashboard view (requires login)
@login_required
def dashboard(request):
    # Render the dashboard.html template, passing the current user
    return render(request, 'dashboard.html', {'user': request.user})

# Materials/resources page (requires login)
@login_required
def materials(request):
    materials = Material.objects.all()
    return render(request, 'materials.html', {'materials': materials})

# Assignments page (requires login)
@login_required
def assignments(request):
    # Render the assignments.html template, passing the current user
    return render(request, 'assignments.html', {'user': request.user})

# Notifications page (requires login)
@login_required
def notifications(request):
    # Render the notifications.html template, passing the current user
    return render(request, 'notifications.html', {'user': request.user})

# Profile page (requires login)
@login_required
def profile(request):
    # Render the profile.html template, passing the current user
    return render(request, 'profile.html', {'user': request.user})

# User login view (handles GET and POST)
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

# User registration view (handles GET and POST)
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

# View for displaying details of a specific resource
def resource_detail(request, pk):
    # Fetch the resource by primary key or return 404 if not found
    resource = get_object_or_404(Resource, pk=pk)
    # Render the material_detail.html template with the resource
    return render(request, 'material_detail.html', {'resource': resource})

def material_detail(request, pk):
    material = get_object_or_404(Material, pk=pk)
    return render(request, 'material_detail.html', {'material': material})


from bs4 import BeautifulSoup

def material_detail(request, pk):
    material = get_object_or_404(Material, pk=pk)
    
    # Parse HTML to extract headings
    soup = BeautifulSoup(material.html_content, 'html.parser')
    headings = []
    
    for i, heading in enumerate(soup.find_all(['h2', 'h3'])):
        heading_id = f"heading-{i}"
        heading['id'] = heading_id  # Add ID to the heading
        
        headings.append({
            'id': heading_id,
            'text': heading.text,
            'tag': heading.name
        })
    
    # Update the HTML with IDs
    material.html_content = str(soup)
    
    # Group headings into hierarchy
    structured_headings = []
    current_h2 = None
    
    for heading in headings:
        if heading['tag'] == 'h2':
            current_h2 = {
                'id': heading['id'],
                'text': heading['text'],
                'children': []
            }
            structured_headings.append(current_h2)
        elif heading['tag'] == 'h3' and current_h2:
            current_h2['children'].append({
                'id': heading['id'],
                'text': heading['text']
            })
    
    context = {
        'material': material,
        'headings': structured_headings,
        # Add previous/next materials if needed
    }
    
    return render(request, 'material_detail.html', context)