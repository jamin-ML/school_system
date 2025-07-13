from django.urls import path
from .api_views import ResourceListCreateView, UserListView, UserDetailView, AssignmentListCreateView, StudentProgressListCreateView, AssignmentDetailView, StudentProgressDetailView, RegisterView, ResourceDownloadView, UserLanguageView, NotificationListView, NotificationMarkReadView, StudentDashboardView, TeacherDashboardView, AssignmentSubmissionListCreateView, AssignmentSubmissionDetailView, ActivityFeedView
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('resources/', ResourceListCreateView.as_view(), name='resource-list-create'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('assignments/', AssignmentListCreateView.as_view(), name='assignment-list-create'),
    path('progress/', StudentProgressListCreateView.as_view(), name='progress-list-create'),
    path('assignments/<int:pk>/', AssignmentDetailView.as_view(), name='assignment-detail'),
    path('progress/<int:pk>/', StudentProgressDetailView.as_view(), name='progress-detail'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', ObtainAuthToken.as_view(), name='login'),
    path('resources/<int:pk>/download/', ResourceDownloadView.as_view(), name='resource-download'),
    path('users/language/', UserLanguageView.as_view(), name='user-language'),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/read/', NotificationMarkReadView.as_view(), name='notification-mark-read'),
    path('dashboard/student/', StudentDashboardView.as_view(), name='student-dashboard'),
    path('dashboard/teacher/', TeacherDashboardView.as_view(), name='teacher-dashboard'),
    path('assignment-submissions/', AssignmentSubmissionListCreateView.as_view(), name='assignment-submission-list-create'),
    path('assignment-submissions/<int:pk>/', AssignmentSubmissionDetailView.as_view(), name='assignment-submission-detail'),
    path('activity-feed/', ActivityFeedView.as_view(), name='activity-feed'),
]
