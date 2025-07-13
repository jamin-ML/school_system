from django.urls import path, include
from learninghub import mpesa_views
from learninghub import views as hub_views

urlpatterns = [
    path('', hub_views.index, name='index'),
    path('dashboard/', hub_views.dashboard, name='dashboard'),
    path('materials/', hub_views.materials, name='materials'),
    path('assignments/', hub_views.assignments, name='assignments'),
    path('notifications/', hub_views.notifications, name='notifications'),
    path('profile/', hub_views.profile, name='profile'),
    path('login/', hub_views.user_login, name='login'),
    path('logout/', hub_views.user_logout, name='logout'),
    path('register/', hub_views.register, name='register'),
    path('mpesa/confirmation/', mpesa_views.mpesa_confirmation, name='mpesa-confirmation'),
    path('mpesa/validation/', mpesa_views.mpesa_validation, name='mpesa-validation'),
]