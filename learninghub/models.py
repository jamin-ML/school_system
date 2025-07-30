# Import model base class and field types from Django
from django.db import models
# Import Django's built-in user model for authentication
from django.contrib.auth.models import AbstractUser
from django_ckeditor_5.fields import CKEditor5Field
from bs4 import BeautifulSoup
from django.utils import timezone


# Custom user model extending Django's AbstractUser
class User(AbstractUser):
    # Define possible roles for users
    ROLE_CHOICES = [
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    # Define language choices for users
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('sw', 'Kiswahili'),
    ]
    # User's role (teacher or student)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    # User's preferred language
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')

    def __str__(self):
        # Return a string representation of the user with their role
        role_display = dict(self.ROLE_CHOICES).get(self.role if isinstance(self.role, str) else str(self.role), self.role)
        return f"{self.username} ({role_display})"

# Model for subjects taught in the system
class Subject(models.Model):
    name = models.CharField(max_length=100)  # e.g., Mathematics
    grade = models.CharField(max_length=20)  # e.g., Grade 8

    def __str__(self):
        return f"{self.name} - {self.grade}"

# Model for topics within a subject
class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)  # e.g., Statistics and Probability

    def __str__(self):
        return self.name

# Model for subtopics within a topic
class SubTopic(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)  # e.g., Data Analysis

    def __str__(self):
        return self.name

# Model for materials/resources related to subtopics
class Material(models.Model):
    subtopic = models.ForeignKey(SubTopic, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    html_content = models.TextField()
    order = models.PositiveIntegerField(blank=True, null=True)  # Order of the material within the subtopic

    def save(self, *args, **kwargs):
        if self.order is None:
            max_order = Material.objects.filter(subtopic=self.subtopic).aggregate(models.Max('order'))['order__max']
            self.order = 1 if max_order is None else max_order + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} (Order: {self.order})"

# Model for notifications sent to users
class Notification(models.Model):
    # User who receives the notification
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    # Notification message
    message = models.CharField(max_length=255)
    # Timestamp when the notification was created
    created_at = models.DateTimeField(auto_now_add=True)
    # Whether the notification has been read
    read = models.BooleanField(default=False)  # type: ignore

    class Meta:
        # Order notifications by most recent first
        ordering = ['-created_at']
        # Ensure uniqueness for user, message, and creation time
        unique_together = ('user', 'message', 'created_at')

    def __str__(self):
        # String representation of the notification
        return f"Notification for {self.user}: {self.message}"
    
