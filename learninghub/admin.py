# Import Django admin module to register models in the admin interface
from django.contrib import admin
# Import models to be registered in the admin site
from .models import User, Resource, Assignment, StudentProgress, ResourcePayment, Material

# Register the User model with the admin site
admin.site.register(User)
# Register the Resource model with the admin site
admin.site.register(Resource)
# Register the Assignment model with the admin site
admin.site.register(Assignment)
# Register the StudentProgress model with the admin site
admin.site.register(StudentProgress)
# Register the ResourcePayment model with the admin site
admin.site.register(ResourcePayment)
admin.site.register(Material)
