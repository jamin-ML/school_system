"""
ASGI config for school project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

# Import os for environment variable management
import os
# Import Django's ASGI application factory
from django.core.asgi import get_asgi_application

# Set the default settings module for the 'school' project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')

# Create the ASGI application object
application = get_asgi_application()
