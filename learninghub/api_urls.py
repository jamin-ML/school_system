# Import Django's path function for defining URL patterns
from django.urls import path
# Import all API views to be used in the URL patterns
from .api_views import ResourceListCreateView, UserListView, UserDetailView, AssignmentListCreateView, StudentProgressListCreateView, AssignmentDetailView, StudentProgressDetailView, RegisterView, ResourceDownloadView, UserLanguageView, NotificationListView, NotificationMarkReadView, StudentDashboardView, TeacherDashboardView, AssignmentSubmissionListCreateView, AssignmentSubmissionDetailView, ActivityFeedView, MaterialDropdownOptionsView, FilteredMaterialsView
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
    # List and create assignments
    path('assignments/', AssignmentListCreateView.as_view(), name='assignment-list-create'),
    # List and create student progress records
    path('progress/', StudentProgressListCreateView.as_view(), name='progress-list-create'),
    # Retrieve, update, or delete a specific assignment
    path('assignments/<int:pk>/', AssignmentDetailView.as_view(), name='assignment-detail'),
    # Retrieve, update, or delete a specific progress record
    path('progress/<int:pk>/', StudentProgressDetailView.as_view(), name='progress-detail'),
    # Register a new user
    path('auth/register/', RegisterView.as_view(), name='register'),
    # Obtain an authentication token (login)
    path('auth/login/', ObtainAuthToken.as_view(), name='login'),
    # Download a resource (requires payment)
    path('resources/<int:pk>/download/', ResourceDownloadView.as_view(), name='resource-download'),
    # Get or update the user's language
    path('users/language/', UserLanguageView.as_view(), name='user-language'),
    # List notifications
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    # Mark a notification as read
    path('notifications/<int:pk>/read/', NotificationMarkReadView.as_view(), name='notification-mark-read'),
    # Student dashboard data
    path('dashboard/student/', StudentDashboardView.as_view(), name='student-dashboard'),
    # Teacher dashboard data
    path('dashboard/teacher/', TeacherDashboardView.as_view(), name='teacher-dashboard'),
    # List and create assignment submissions
    path('assignment-submissions/', AssignmentSubmissionListCreateView.as_view(), name='assignment-submission-list-create'),
    # Retrieve a specific assignment submission
    path('assignment-submissions/<int:pk>/', AssignmentSubmissionDetailView.as_view(), name='assignment-submission-detail'),
    # Activity feed for the user
    path('activity-feed/', ActivityFeedView.as_view(), name='activity-feed'),
    # Dropdown options for materials
    path('materials/options/', MaterialDropdownOptionsView.as_view(), name='material-dropdown-options'),
    # Filtered materials list
    path('materials/filter/', FilteredMaterialsView.as_view(), name='filtered-materials'),
]
