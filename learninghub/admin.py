from django.contrib import admin
from .models import (
    User, Subject, Topic, SubTopic, Material,
    Course, StudentProfile, StudentCourseProgress,
    StudentMaterialProgress, Badge, StudentBadge,
    Activity, WeeklyActivity, Skill, StudentSkill,
    Event, Notification
)

# ----------------------
# SUBJECT & MATERIAL STRUCTURE
# ----------------------

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade')
    list_filter = ('grade',)
    search_fields = ('name', 'grade')


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')
    list_filter = ('subject',)
    search_fields = ('name',)


@admin.register(SubTopic)
class SubTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'get_subject')
    list_filter = ('topic',)
    search_fields = ('name',)

    def get_subject(self, obj):
        return obj.topic.subject
    get_subject.short_description = 'Subject'


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'subtopic', 'get_topic', 'get_subject')
    list_filter = ('subtopic',)  # ✅ Changed
    search_fields = ('title', 'html_content', 'subtopic__name')
    ordering = ['subtopic__name', 'order']  # ✅ Changed

    def get_topic(self, obj):
        return obj.subtopic.topic
    get_topic.short_description = 'Topic'

    def get_subject(self, obj):
        return obj.subtopic.topic.subject
    get_subject.short_description = 'Subject'





# ----------------------
# COURSE & STUDENT PROGRESS
# ----------------------

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'created_at')
    list_filter = ('subject', 'created_at')
    search_fields = ('title', 'subject__name')
    ordering = ['subject', 'title']


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'xp', 'streak', 'last_active')
    search_fields = ('user__username',)
    list_filter = ('level', 'last_active')


@admin.register(StudentCourseProgress)
class StudentCourseProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'progress', 'next_lesson', 'deadline')
    list_filter = ('course', 'progress')
    search_fields = ('student__user__username', 'course__title')
    ordering = ['course', 'student']


@admin.register(StudentMaterialProgress)
class StudentMaterialProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'material', 'completed', 'completed_at')
    list_filter = ('completed', 'material__subtopic',)  # ✅ Changed
    search_fields = (
        'student__user__username',
        'material__title',
        'material__subtopic__topic__name'
    )

# ----------------------
# BADGES, SKILLS, AND ACTIVITIES
# ----------------------

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'description')
    search_fields = ('name',)


@admin.register(StudentBadge)
class StudentBadgeAdmin(admin.ModelAdmin):
    list_display = ('student', 'badge', 'earned_at', 'earned')
    list_filter = ('earned', 'badge')
    search_fields = ('student__user__username', 'badge__name')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('student', 'description', 'timestamp', 'icon')
    list_filter = ('timestamp',)
    search_fields = ('student__user__username', 'description')


@admin.register(WeeklyActivity)
class WeeklyActivityAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'minutes_learned')
    list_filter = ('date',)
    search_fields = ('student__user__username',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(StudentSkill)
class StudentSkillAdmin(admin.ModelAdmin):
    list_display = ('student', 'skill', 'level')
    list_filter = ('skill',)
    search_fields = ('student__user__username', 'skill__name')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'date_time', 'student')
    list_filter = ('event_type', 'date_time')
    search_fields = ('title', 'student__user__username')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'read')
    list_filter = ('read', 'created_at')
    search_fields = ('user__username', 'message')

admin.site.register(User)  # Register User model for admin interface