from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import date, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

# ----------------------
# CUSTOM USER MODEL
# ----------------------

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
    language = models.CharField(max_length=2,
                                choices=LANGUAGE_CHOICES, default='en')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


# ----------------------
# SUBJECT & MATERIAL STRUCTURE
# ----------------------
class Subject(models.Model):
    name = models.CharField(max_length=100)  # e.g., Mathematics
    grade = models.CharField(max_length=20)  # e.g., Grade 8
    subject_image = models.ImageField(upload_to='subjects_image',null=True)
    description = models.CharField(max_length=200,null=True)

    def __str__(self):
        return f"{self.name} - {self.grade}"


class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)  # e.g., Probability
    topic_image = models.ImageField(upload_to='topic_images',null=True)
    description = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name


class SubTopic(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)  # e.g., Data Analysis
    def __str__(self):
        return self.name


class Material(models.Model):
    course = models.ForeignKey(
        'Course', on_delete=models.CASCADE, related_name='materials', null=True, blank=True
    )
    subtopic = models.ForeignKey(SubTopic, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    html_content = models.TextField()
    order = models.PositiveIntegerField(blank=True, null=True)
    xp_value = models.PositiveIntegerField(default=50)

    def save(self, *args, **kwargs):
        if self.order is None:
            max_order = Material.objects.filter(course=self.course).aggregate(models.Max('order'))['order__max']
            self.order = 1 if max_order is None else max_order + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} (Order: {self.order})"

    class Meta:
        ordering = ['order', 'id']


# ----------------------
# STUDENT PROFILE & GAMIFICATION
# ----------------------


class StudentProfile(models.Model):
    user = models.OneToOneField(settings.
                                AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.URLField(max_length=200, blank=True)
    streak = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    xp = models.PositiveIntegerField(default=0)
    xp_to_next_level = models.PositiveIntegerField(default=600)
    rank = models.PositiveIntegerField(default=0)
    last_active = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def add_xp(self, amount):
        """Award XP and handle level-ups"""
        self.xp += amount
        self.points += amount  # Points = total XP
        leveled_up = False

        # Handle multiple level-ups
        while self.xp >= self.xp_to_next_level:
            self.xp -= self.xp_to_next_level
            self.level += 1
            self.xp_to_next_level = int(self.xp_to_next_level * 1.2) 
            leveled_up = True

        self.save()
        return leveled_up

    def update_streak(self):
        """Update daily streak"""
        today = date.today()

        if self.last_active == today:
            return

        if self.last_active == today - timedelta(days=1):
            self.streak += 1
        else:
            self.streak = 1  # Reset streak

        self.last_active = today
        self.save()


class Course(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class StudentCourseProgress(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.PositiveIntegerField(default=0)  # Percentage
    next_lesson = models.ForeignKey(
        Material,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_lesson_progress'
    )
    deadline = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.user.username} - {self.course.title}"

class StudentMaterialProgress(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'material')

    def __str__(self):
        return f"{self.student.user.username} - {self.material.title}"


class Badge(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=10)  # Emoji or icon code
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class StudentBadge(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    earned = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'badge')

    def __str__(self):
        return f"{self.student.user.username} - {self.badge.name}"


class Activity(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    icon = models.CharField(max_length=10, blank=True)  # Emoji for activity type

    def __str__(self):
        return f"{self.student.user.username} - {self.description}"


class WeeklyActivity(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    date = models.DateField()
    minutes_learned = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.user.username} - {self.date}"


class Skill(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class StudentSkill(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=0)  # 0-100 scale

    class Meta:
        unique_together = ('student', 'skill')

    def __str__(self):
        return f"{self.student.user.username} - {self.skill.name}"


class Event(models.Model):
    EVENT_TYPES = (
        ('EXAM', 'Exam'),
        ('LIVE', 'Live Session'),
        ('ASSIGNMENT', 'Assignment'),
    )
    title = models.CharField(max_length=100)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    date_time = models.DateTimeField()
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.event_type}"


# ----------------------
# NOTIFICATIONS
# ----------------------
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'message', 'created_at')

    def __str__(self):
        return f"Notification for {self.user}: {self.message}"


# ----------------------
# SIGNALS FOR AUTOMATION
# ----------------------
@receiver(post_save, sender=StudentMaterialProgress)
def handle_material_completion(sender, instance, created, **kwargs):
    """Award XP and update course progress when a material is completed"""
    if instance.completed:
        student = instance.student
        material = instance.material

        # 1. Award XP
        leveled_up = student.add_xp(50)
        student.update_streak()

        # 2. Update course progress
        course = Course.objects.filter(subject=material.subtopic.topic.subject).first()
        if course:
            total_materials = Material.objects.filter(
                subtopic__topic__subject=course.subject
            ).count()
            completed_materials = StudentMaterialProgress.objects.filter(
                student=student, completed=True,
                material__subtopic__topic__subject=course.subject
            ).count()
            progress_percent = int((completed_materials / total_materials) * 100)

            progress_obj, _ = StudentCourseProgress.objects.get_or_create(student=student, course=course)
            progress_obj.progress = progress_percent

            # Find next lesson
            next_material = Material.objects.filter(
                subtopic__topic__subject=course.subject
            ).exclude(id__in=StudentMaterialProgress.objects.filter(
                student=student, completed=True
            ).values_list('material_id', flat=True)).order_by('order').first()

            progress_obj.next_lesson = next_material
            progress_obj.save()

        # 3. Award streak badge
        if student.streak == 7:
            badge, _ = Badge.objects.get_or_create(
                name="7-Day Streak", defaults={"icon": "🔥", "description": "Learned 7 days in a row"}
            )
            StudentBadge.objects.get_or_create(student=student, badge=badge)

        # 4. Award level badge
        if leveled_up:
            badge, _ = Badge.objects.get_or_create(
                name=f"Level {student.level}", defaults={"icon": "⭐", "description": f"Reached Level {student.level}"}
            )
            StudentBadge.objects.get_or_create(student=student, badge=badge)
