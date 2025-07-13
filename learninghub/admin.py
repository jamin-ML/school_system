from django.contrib import admin
from .models import User, Resource, Assignment, StudentProgress, ResourcePayment

admin.site.register(User)
admin.site.register(Resource)
admin.site.register(Assignment)
admin.site.register(StudentProgress)
admin.site.register(ResourcePayment)
