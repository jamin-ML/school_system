# Import Django REST Framework's serializer base classes
from rest_framework import serializers
# Import models to be serialized
from .models import User, Material, Notification

# Serializer for the custom User model
class UserSerializer(serializers.ModelSerializer):
    # Password field is write-only (not returned in API responses)
    password = serializers.CharField(write_only=True, required=False)
    # Language field uses the choices defined in the User model
    language = serializers.ChoiceField(choices=User.LANGUAGE_CHOICES, required=False)

    class Meta:
        # Model to serialize
        model = User
        # Fields to include in the serialized output
        fields = ['id', 'username', 'email', 'role', 'password', 'language']

    def create(self, validated_data):
        # Custom user creation to handle password hashing
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user 

# Serializer for the Resource model
class ResourceSerializer(serializers.ModelSerializer):
    # Add a computed field to indicate if the resource is HTML contentclass ResourceSerializer(serializers.ModelSerializer):
    is_html = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()

    class Meta:
        model = Material
        fields = ['id', 'title', 'order', 'html_content', 'xp_value', 'is_html', 'subject']

    def get_is_html(self, obj):
        return bool(obj.html_content)

    def get_subject(self, obj):
        return obj.subtopic.topic.subject.name if obj.subtopic and obj.subtopic.topic and obj.subtopic.topic.subject else None
# Serializer for the Notification model
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'  # Serialize all fields

from rest_framework import serializers
from .models import (
    StudentProfile, StudentCourseProgress, StudentBadge,
    Activity, WeeklyActivity, StudentSkill, Event, Course
)

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = [
            "user", "avatar", "streak", "points", "level",
            "xp", "xp_to_next_level", "rank"
        ]


class CourseProgressSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)
    subject = serializers.CharField(source="course.subject.name", read_only=True)

    class Meta:
        model = StudentCourseProgress
        fields = ["course_title", "subject", "progress", "next_lesson", "deadline"]


class BadgeSerializer(serializers.ModelSerializer):
    badge_name = serializers.CharField(source="badge.name", read_only=True)
    badge_icon = serializers.CharField(source="badge.icon", read_only=True)

    class Meta:
        model = StudentBadge
        fields = ["badge_name", "badge_icon", "earned_at", "earned"]


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ["description", "icon", "timestamp"]


class WeeklyActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyActivity
        fields = ["date", "minutes_learned"]


class SkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source="skill.name", read_only=True)

    class Meta:
        model = StudentSkill
        fields = ["skill_name", "level"]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["title", "event_type", "date_time"]
