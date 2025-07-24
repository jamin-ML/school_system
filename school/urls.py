"""
URL configuration for school project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Import Django admin and URL utilities
from django.contrib import admin
from django.urls import path, include
# Import views for M-Pesa and main hub (not directly used here, but may be for custom endpoints)
from learninghub import mpesa_views
from learninghub import views as hub_views

# Main URL patterns for the project
urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    # Main app URLs (landing, dashboard, etc.)
    path('', include('learninghub.urls')),
    # API endpoints for the app
    path('api/', include('learninghub.api_urls')),
    # DRF's built-in login/logout views for the browsable API
    path('api-auth/', include('rest_framework.urls')),
]

# Import settings and static utilities for serving static/media files in development
from django.conf import settings
from django.conf.urls.static import static

# Serve static and media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)