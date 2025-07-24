# Import the path and include functions for defining URL patterns
from django.urls import path, include
# Import mpesa_views for handling M-Pesa related endpoints
from learninghub import mpesa_views
# Import views from learninghub, aliased as hub_views for clarity
from learninghub import views as hub_views

# Define the URL patterns for the learninghub app
urlpatterns = [
    # Home page, handled by the index view
    path('', hub_views.index, name='index'),
    # Dashboard page for logged-in users
    path('dashboard/', hub_views.dashboard, name='dashboard'),
    # List of all materials/resources
    path('materials/', hub_views.materials, name='materials'),
    # List of assignments
    path('assignments/', hub_views.assignments, name='assignments'),
    # Notifications page
    path('notifications/', hub_views.notifications, name='notifications'),
    # User profile page
    path('profile/', hub_views.profile, name='profile'),
    # Login page
    path('login/', hub_views.user_login, name='login'),
    # Login page for accounts (Django convention)
    path('accounts/login/', hub_views.user_login, name='accounts-login'),
    # Logout endpoint for accounts
    path('accounts/logout/', hub_views.user_logout, name='account_logout'),
    # User registration page
    path('register/', hub_views.register, name='register'),
    # M-Pesa payment confirmation endpoint (for receiving payment confirmations from M-Pesa API)
    path('mpesa/confirmation/', mpesa_views.mpesa_confirmation, name='mpesa-confirmation'),
    # M-Pesa payment validation endpoint (for validating payment requests from M-Pesa API)
    path('mpesa/validation/', mpesa_views.mpesa_validation, name='mpesa-validation'),
    # Detail page for a specific material/resource, identified by its primary key (pk)
    # path('materials/<int:pk>/', hub_views.resource_detail, name='resource_detail'),
]

urlpatterns += [
    path('materials/<int:pk>/', hub_views.material_detail, name='material_detail'),
]