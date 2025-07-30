# Import Django admin module to register models in the admin interface
from django.contrib import admin
# Import models to be registered in the admin site
from .models import User,SubTopic,Topic,Subject, Material

# Register the User model with the admin site
admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Subject)
admin.site.register(SubTopic)

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'html_content', 'get_subject', 'order', 'subtopic')
    search_fields = ('title', 'html_content')
    fields = ('title', 'html_content', 'subtopic')
    ordering = ['subtopic', 'order']

    def get_subject(self, obj):
        return obj.subtopic.topic.subject  # follow the relationship chain
    get_subject.short_description = 'Subject'

