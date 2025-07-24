"""
WSGI config for school project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

# Import os for environment variable management
import os
# Import Django's WSGI application factory
from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'school' project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')

# Create the WSGI application object
application = get_wsgi_application()
