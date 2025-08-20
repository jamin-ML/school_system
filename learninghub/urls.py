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
    # List of all materials/resources
    path('materials/', hub_views.subject_list, name='subject_list'),
    # Login page
    path('login/', hub_views.user_login, name='user_login'),
    # Logout endpoint for accounts
    path('accounts/logout/', hub_views.user_logout, name='account_logout'),
    # User registration page
    path('register/', hub_views.student_registration, name='user_register'),
    # M-Pesa payment confirmation endpoint (for receiving payment confirmations from M-Pesa API)
    path('mpesa/confirmation/', mpesa_views.mpesa_confirmation, name='mpesa-confirmation'),
    # M-Pesa payment validation endpoint (for validating payment requests from M-Pesa API)
    path('mpesa/validation/', mpesa_views.mpesa_validation, name='mpesa-validation'),
    # Detail page for a specific material/resource, identified by its primary key (pk)
    path('dashboard/', hub_views.dashboard_view, name='dashboard'),
    path('material/', hub_views.complete_material, name='complete_material'),
    path('courses/', hub_views.course_list, name='course_list'),
    path('courses/enroll/', hub_views.enroll_course, name='enroll_course'),
    
    path('subject/<int:subject_id>/topic/', hub_views.topic_list, name='topic_list'),
    path('topic/<int:topic_id>/first-material/', hub_views.material_detail_first, name='material_detail_first'),
    path('material/<int:pk>/', hub_views.material_detail, name='material_detail'),
]

