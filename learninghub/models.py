from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('sw', 'Kiswahili'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')

    def __str__(self):
        role_display = dict(self.ROLE_CHOICES).get(self.role if isinstance(self.role, str) else str(self.role), self.role)
        return f"{self.username} ({role_display})"

class Resource(models.Model):
    RESOURCE_TYPE_CHOICES = [
        ('pdf', 'PDF'),
        ('docx', 'DOCX'),
        ('ppt', 'PPT'),
        ('mp4', 'MP4'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='materials/')
    subject = models.CharField(max_length=100)
    grade = models.CharField(max_length=50)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPE_CHOICES)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('draft', 'Draft'), ('published', 'Published')], default='draft')
    view_count = models.PositiveIntegerField(default=0) # type: ignore
    download_count = models.PositiveIntegerField(default=0) # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Assignment(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='assignments')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    grade = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {str(self.assigned_to)}"

class StudentProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    progress = models.FloatField(default=0)  # type: ignore
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'resource')

    def __str__(self):
        return f"{str(self.user)} - {str(self.resource)} ({self.progress}%)"

class ResourcePayment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)  # type: ignore   
    paid_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'resource')

    def __str__(self):
        return f"{self.student} - {self.resource} - Paid: {self.paid}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # type: ignore

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'message', 'created_at')

    def __str__(self):
        return f"{str(self.user)}: {self.message} ({'Read' if self.read else 'Unread'})"

class AssignmentSubmission(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
    ]
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='assignment_submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    grade = models.CharField(max_length=10, blank=True)
    feedback = models.TextField(blank=True)

    class Meta:
        unique_together = ('assignment', 'student')
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{str(self.assignment)} - {self.student} ({self.status})"