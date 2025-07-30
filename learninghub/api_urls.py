# Import Django's path function for defining URL patterns
from django.urls import path
# Import all API views to be used in the URL patterns
from .api_views import ResourceListCreateView, UserListView, UserDetailView, RegisterView,  UserLanguageView, NotificationListView, NotificationMarkReadView,  FilteredMaterialsView
# Import ObtainAuthToken for token-based authentication
from rest_framework.authtoken.views import ObtainAuthToken

# Define the URL patterns for the API endpoints
urlpatterns = [
    # List and create resources
    path('resources/', ResourceListCreateView.as_view(), name='resource-list-create'),
    # List all users
    path('users/', UserListView.as_view(), name='user-list'),
    # Retrieve a specific user by ID
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    # Register a new user
    path('auth/register/', RegisterView.as_view(), name='register'),
    # Obtain an authentication token (login)
    path('auth/login/', ObtainAuthToken.as_view(), name='login'),
    # Download a resource (requires payment)
    # Get or update the user's language
    path('users/language/', UserLanguageView.as_view(), name='user-language'),
    # List notifications
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    # Mark a notification as read
    path('notifications/<int:pk>/read/', NotificationMarkReadView.as_view(), name='notification-mark-read'),
    # Student dashboard data
    # Filtered materials list
    path('materials/filter/', FilteredMaterialsView.as_view(), name='filtered-materials'),
    
]
