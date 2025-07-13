from django.contrib import admin
from .models import Materials, ClassLevel, Subjects, StudentProgress,TeacherResource

@admin.register(Materials)
class MaterialsAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'created_at', 'views')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'teacher')
    ordering = ('-created_at',)

admin.site.register(TeacherResource)
admin.site.register(Subjects)
admin.site.register(ClassLevel)
