from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from .models import User, StudentMaterialProgress, StudentCourseProgress, StudentProfile, Badge, StudentBadge, Material, Course

@receiver(post_save, sender=StudentMaterialProgress)
def handle_material_completion(sender, instance, created, **kwargs):
    """Award XP and update course progress when a material is completed"""
    if instance.completed:
        student = instance.student
        material = instance.material
        course = material.course  # Direct access to course

        # Check if student is enrolled in the course
        try:
            progress_obj = StudentCourseProgress.objects.get(student=student, course=course)
        except ObjectDoesNotExist:
            # Skip if not enrolled (no auto-enrollment)
            return

        # 1. Award XP
        leveled_up = student.add_xp(material.xp_value)  # Consider making XP dynamic via Material field
        student.update_streak()

        # 2. Update course progress
        total_materials = Material.objects.filter(course=course).count()
        completed_materials = StudentMaterialProgress.objects.filter(
            student=student, completed=True, material__course=course
        ).count()
        progress_percent = int((completed_materials / total_materials) * 100) if total_materials > 0 else 0

        progress_obj.progress = progress_percent

        # Find next lesson
        next_material = Material.objects.filter(
            course=course
        ).exclude(
            id__in=StudentMaterialProgress.objects.filter(
                student=student, completed=True
            ).values_list('material_id', flat=True)
        ).order_by('order').first()

        progress_obj.next_lesson = next_material
        progress_obj.save()

        # 3. Award course completion badge
        if progress_percent == 100:
            badge, _ = Badge.objects.get_or_create(
                name="Course Completer",
                defaults={"icon": "🏅", "description": f"Completed {course.title}"}
            )
            StudentBadge.objects.get_or_create(student=student, badge=badge)

        # 4. Award streak badge
        if student.streak == 7:
            badge, _ = Badge.objects.get_or_create(
                name="7-Day Streak",
                defaults={"icon": "🔥", "description": "Learned 7 days in a row"}
            )
            StudentBadge.objects.get_or_create(student=student, badge=badge)

        # 5. Award level badge
        if leveled_up:
            badge, _ = Badge.objects.get_or_create(
                name=f"Level {student.level}",
                defaults={"icon": "⭐", "description": f"Reached Level {student.level}"}
            )
            StudentBadge.objects.get_or_create(student=student, badge=badge)

        if progress_percent >= 50:
            badge, _ = Badge.objects.get_or_create(
                name="Halfway There",
                defaults={"icon": "🔥", "description": f"Reached 50% in {course.title}"}
            )
            StudentBadge.objects.get_or_create(student=student, badge=badge)

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)