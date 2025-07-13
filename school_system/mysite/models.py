from django.db import models
from django.contrib.auth.models import User

class ClassLevel(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Subjects(models.Model):
    name = models.CharField(max_length=100)
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.class_level.name})'

class Materials(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='materials/')
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/')
    views = models.PositiveIntegerField(default=0)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class StudentProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(Materials, on_delete=models.CASCADE)
    progress = models.FloatField(default=0.0)  # Progress in percentage
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'material')

    def __str__(self):
        return f'{self.student.username} - {self.material.title} ({self.progress}%)'    
    

class TeacherResource(models.Model):
    RESOURCE_TYPES = (
        ('video', 'Video'),
        ('image', 'Image'),
        ('doc', 'Document'),
        ('ppt', 'Presentation'),
        ('audio', 'Audio'),
        ('other', 'Other'),
    )
    
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES)
    file = models.FileField(upload_to='teacher_resources/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100, blank=True)
    grade_level = models.CharField(max_length=50, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    content_body = models.TextField(blank=True, null=True)  # For rich text content


    def __str__(self):
        return f"{self.title}- {self.content_body}"

    def get_file_extension(self):
        return self.file.name.split('.')[-1].lower()