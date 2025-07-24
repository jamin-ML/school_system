# Import model base class and field types from Django
from pyexpat import model  # (Unused import, can be removed)
from django.db import models
# Import Django's built-in user model for authentication
from django.contrib.auth.models import AbstractUser

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

# Model representing a learning resource (e.g., PDF, video)
class Resource(models.Model):
    # Resource type choices
    RESOURCE_TYPE_CHOICES = [
        ('pdf', 'PDF'),
        ('docx', 'DOCX'),
        ('ppt', 'PPT'),
        ('mp4', 'MP4'),
        ('other', 'Other'),
    ]
    # Title of the resource
    title = models.CharField(max_length=255)

    # Image of the resource
    image = models.ImageField(upload_to='materials/', blank=True, null=True)
    # Description of the resource
    description = models.TextField(blank=True)
    # File associated with the resource (optional)
    file = models.FileField(upload_to='materials/', blank=True, null=True)
    # HTML content for the resource (optional)
    html_content = models.TextField(blank=True, null=True)
    # Subject the resource belongs to
    subject = models.CharField(max_length=100)
    # Grade level for the resource
    grade = models.CharField(max_length=50)
    # Type of resource (pdf, docx, etc.)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPE_CHOICES)
    # User who uploaded the resource
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # Status of the resource (draft or published)
    status = models.CharField(max_length=10, choices=[('draft', 'Draft'), ('published', 'Published')], default='draft')
    # Number of times the resource has been viewed
    view_count = models.PositiveIntegerField(default=0) # type: ignore
    # Number of times the resource has been downloaded
    download_count = models.PositiveIntegerField(default=0) # type: ignore
    # Timestamp when the resource was created
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_html(self):
        # Returns True if the resource is HTML content only
        return bool(self.html_content and not self.file)

    def __str__(self):
        # String representation of the resource
        return self.title

# Model representing an assignment given to a student
class Assignment(models.Model):
    # Status choices for the assignment
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
    ]
    # Title of the assignment
    title = models.CharField(max_length=255)
    # Description of the assignment
    description = models.TextField(blank=True)
    # Due date for the assignment
    due_date = models.DateTimeField()
    # Resource associated with the assignment
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='assignments')
    # User (student) to whom the assignment is assigned
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    # Status of the assignment
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    # Grade received for the assignment (optional)
    grade = models.CharField(max_length=10, blank=True)
    # Timestamp when the assignment was created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # String representation of the assignment
        return f"{self.title} - {str(self.assigned_to)}"

# Model tracking a student's progress on a resource
class StudentProgress(models.Model):
    # User (student) making progress
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Resource being tracked
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    # Progress percentage (0-100)
    progress = models.FloatField(default=0)  # type: ignore
    # Last time the resource was accessed
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensure each user-resource pair is unique
        unique_together = ('user', 'resource')

    def __str__(self):
        # String representation of the progress
        return f"{str(self.user)} - {str(self.resource)} ({self.progress}%)"

# Model representing payment for a resource by a student
class ResourcePayment(models.Model):
    # Student who made the payment
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    # Resource that was paid for
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    # Whether the payment was made
    paid = models.BooleanField(default=False)  # type: ignore   
    # Timestamp when the payment was made
    paid_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure each student-resource pair is unique
        unique_together = ('student', 'resource')

    def __str__(self):
        # String representation of the payment
        return f"{self.student} - {self.resource} - Paid: {self.paid}"

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

# Model for assignment submissions by students
class AssignmentSubmission(models.Model):
    # Status choices for the submission
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
    ]
    # Assignment being submitted
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    # Student who submitted the assignment
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    # File uploaded as the submission
    file = models.FileField(upload_to='assignment_submissions/')
    # Timestamp when the submission was made
    submitted_at = models.DateTimeField(auto_now_add=True)
    # Status of the submission
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    # Grade received for the submission (optional)
    grade = models.CharField(max_length=10, blank=True)
    # Feedback for the submission (optional)
    feedback = models.TextField(blank=True)

    class Meta:
        # Ensure each assignment-student pair is unique
        unique_together = ('assignment', 'student')
        # Order submissions by most recent first
        ordering = ['-submitted_at']

    def __str__(self):
        # String representation of the submission
        return f"Submission by {self.student} for {self.assignment}"

class Material(models.Model):
    title = models.CharField(max_length=200)
    html_content = models.TextField()  # Store your HTML here

    def __str__(self):
        return self.title