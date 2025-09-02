from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import  login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Avg, F
from django.contrib import messages
from django.utils import timezone
from .forms import StudentRegistrationForm
from .models import (
    Material, Topic, Subject, SubTopic,
    StudentProfile, StudentCourseProgress,
    StudentBadge, WeeklyActivity, Activity,
    Notification, StudentMaterialProgress, Course
)
from django.db.models import Q,Count


# ------------------ AUTH VIEWS ------------------


#----------------------------------------------
# User login view which uses Custom user Models
#----------------------------------------------
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('subject_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('index')


def student_registration(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'student'
            user.save()
            login(request, user)
            messages.success(request, "Registration successful! Please select your course.")
            return redirect('enroll_course')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = StudentRegistrationForm()
    return render(request, 'student_registration.html', {'form': form})

#----------------------------------------------
# Home page view
#----------------------------------------------
def index(request):
    return render(request, 'index.html')

#----------------------------------------------
# Materials page view
#----------------------------------------------
# Every user can see and open the materials page
def subject_list(request):
    all_subjects = Subject.objects.all()

    # Dropdown choices
    subject_choices = all_subjects.values_list('id', 'name')
    grade_choices = all_subjects.values_list('grade', flat=True).distinct()

    # Get filter values
    search_query = request.GET.get('search', '').strip()
    selected_subject = request.GET.get('subject') or None
    selected_grade = request.GET.get('grade') or None

    # Start with all subjects
    filtered_subjects = all_subjects

    # Apply search filter
    if search_query:
        filtered_subjects = filtered_subjects.filter(
            Q(name__icontains=search_query) | Q(grade__icontains=search_query)
        )

    # Apply dropdown filters
    if selected_subject:
        filtered_subjects = filtered_subjects.filter(id=selected_subject)
    if selected_grade:
        filtered_subjects = filtered_subjects.filter(grade=selected_grade)

    return render(request, 'materials.html', {
        'subjects': filtered_subjects,
        'subject_choices': subject_choices,
        'grade_choices': grade_choices,
        'selected_subject': selected_subject,
        'selected_grade': selected_grade,
        'search_query': search_query,
    })

def topic_list(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    #get all topics related to the subject
    topics = (
        Topic.objects.filter(subject=subject)
        .annotate(material_count = Count('subtopic__material'))#Check if they have materials
        .filter(material_count__gt = 0)  # Only include topics with materials
    )

    return render(request,'topics.html',
                  {
                      'topics':topics,
                      'subject': subject,
                  })
    
# ------------------ MATERIAL DETAIL ------------------
@login_required
def material_detail(request, pk):
    material = get_object_or_404(Material, pk=pk)
    subtopic = material.subtopic
    topic = subtopic.topic

    subtopics = topic.subtopic_set.prefetch_related('material_set').all()

    # Find previous/next material within the same topic
    all_materials = list(Material.objects.filter(subtopic__topic=topic).order_by('order', 'id'))
    materials_list = all_materials
    try:
        idx = materials_list.index(material)
    except ValueError:
        # If current material not in ordered list, re-fetch exact instance and compute
        materials_list_ids = [m.id for m in materials_list]
        if material.id not in materials_list_ids:
            materials_list.append(material)
            materials_list.sort(key=lambda m: (m.order or 0, m.id))
        idx = materials_list.index(material)

    previous_material = materials_list[idx - 1] if idx > 0 else None
    next_material = materials_list[idx + 1] if idx < len(materials_list) - 1 else None

    return render(request, 'material_detail.html', {
        'current_material': material,
        'subtopics': subtopics,
        'topic': topic,
        'previous_material': previous_material,
        'next_material': next_material,
    })

def material_detail_first(request, topic_id):
    
    topic = get_object_or_404(Topic, id=topic_id)

    first_material = (
        Material.objects.filter(subtopic__topic=topic)
        .order_by('order', 'id')
        .first()
    )

    if first_material:
        return redirect('material_detail', pk=first_material.pk)
    else:
        messages.warning(request, "No materials available for this topic.")
        return redirect('topic_list', subject_id=topic.subject.id)

# ------------------ DASHBOARD VIEW ------------------
@login_required
def dashboard_view(request):
    user = request.user
    if user.role != 'student':
        messages.error(request, "This dashboard is only for students.")
        return redirect('user_register')

    try:
        student = user.studentprofile
    except StudentProfile.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('user_register')

    xp_progress = student.xp
    xp_needed = student.xp_to_next_level
    xp_percentage = round((xp_progress / xp_needed) * 100, 2) if xp_needed > 0 else 0
    xp_remaining = max(xp_needed - xp_progress, 0)

    unread_count = Notification.objects.filter(user=user, read=False).count()
    user_data = {
        "name": student.user.username,
        "avatar": student.avatar or "https://i.pravatar.cc/150?img=5",
        "streak": student.streak,
        "points": student.points,
        "level": student.level,
        "xpProgress": student.xp,
        "xpNeeded": student.xp_to_next_level,
        "rank": student.rank,
        "completionPercentage": round(
            StudentCourseProgress.objects.filter(student=student).aggregate(
                avg=Avg('progress')
            )['avg'] or 0
        ),
        "todayGoal": {"completed": 2, "total": 3},  # Placeholder
    }


    courses = StudentCourseProgress.objects.filter(student=student).select_related(
        'course__subject', 'next_lesson'
    ).values(
        title=F('course__title'),
        courseProgress=F('progress'),
        nextLesson=F('next_lesson__title'),  # Access title via ForeignKey
        nextLessonId=F('next_lesson__id'),   # Add ID for linking
        courcedeadline=F('deadline')
    )


    leaderboard = StudentProfile.objects.order_by('-points')[:3].select_related('user').values(
        name=F('user__username'), studentpoints=F('points')
    )

    badges = StudentBadge.objects.filter(student=student).select_related('badge').values(
        name=F('badge__name'), activtyicon=F('badge__icon'), budgearned=F('earned')
    )

    weekly_data = WeeklyActivity.objects.filter(student=student).order_by('date').values_list('minutes_learned', flat=True)

    activity_feed = Activity.objects.filter(student=student).order_by('-timestamp')[:5].values(
        badgdescription=F('description'), activitytimestamp=F('timestamp'), activtyicon=F('icon')
    )

    return render(request, "dashboard.html", {
        "user_data": user_data,
        "courses": courses,
        "leaderboard": leaderboard,
        "badges": badges,
        "weekly_data": weekly_data,
        "activity_feed": activity_feed,
        "unread_count": unread_count,
    })

# ------------------ COURSE ENROLLMENT ------------------
@login_required
def enroll_course(request):
    if request.user.role != 'student':
        messages.error(request, "Only students can enroll in courses.")
        return redirect('index')

    try:
        student_profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('course_list')

    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        try:
            course = Course.objects.get(id=course_id)
            progress, created = StudentCourseProgress.objects.get_or_create(
                student=student_profile,
                course=course,
                defaults={'progress': 0}
            )
            if created:
                first_material = Material.objects.filter(course=course).order_by('order').first()
                progress.next_lesson = first_material  # Set to Material instance or None
                progress.save()
                messages.success(request, f"Successfully enrolled in {course.title}!")
            else:
                messages.info(request, f"You are already enrolled in {course.title}.")
        except Course.DoesNotExist:
            messages.error(request, "Course not found.")
        return redirect('course_list')

    enrolled_courses = StudentCourseProgress.objects.filter(student=student_profile).values_list('course_id', flat=True)
    available_courses = Course.objects.exclude(id__in=enrolled_courses).select_related('subject')
    return render(request, 'enroll_course.html', {'courses': available_courses})

# ------------------ COMPLETE MATERIAL ------------------
@login_required
def complete_material(request, material_id):
    if request.method != 'POST':
        return redirect('material_detail', pk=material_id)

    if request.user.role != 'student':
        messages.error(request, "Only students can complete materials.")
        return redirect('course_list')

    try:
        student = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('course_list')

    material = get_object_or_404(Material, id=material_id)
    if not StudentCourseProgress.objects.filter(student=student, course=material.course).exists():
        messages.error(request, "You are not enrolled in this course.")
        return redirect('course_list')

    progress, created = StudentMaterialProgress.objects.get_or_create(
        student=student, material=material, defaults={'completed': True, 'completed_at': timezone.now()}
    )
    if not created and not progress.completed:
        progress.completed = True
        progress.completed_at = timezone.now()
        progress.save()

    # Redirect to next material if available, else course list
    next_material = Material.objects.filter(course=material.course, order__gt=material.order).order_by('order').first()
    if next_material:
        return redirect('material_detail', pk=next_material.id)
    return redirect('course_list')


@login_required
def course_list(request):
    if request.user.role != 'student':
        messages.error(request, "Only students can view courses.")
        return redirect('user_login')  # Replace with your home URL

    try:
        student = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('index')

    # Fetch enrolled courses with related course, subject, and next_lesson
    enrolled_courses = StudentCourseProgress.objects.filter(student=student).select_related(
        'course__subject', 'next_lesson'
    ).values(
        'course__id',
        'course__title',
        'course__subject__name',
        'progress',
        'next_lesson__id',
        'next_lesson__title',
        'deadline'
    )

    # Fetch available courses (not enrolled) with related subject
    enrolled_course_ids = enrolled_courses.values_list('course__id', flat=True)
    available_courses = Course.objects.exclude(id__in=enrolled_course_ids).select_related('subject')

    return render(request, 'course_list.html', {
        'enrolled_courses': enrolled_courses,
        'available_courses': available_courses,
    })