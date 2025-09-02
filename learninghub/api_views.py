# Import Django REST Framework generic views and permissions
from rest_framework import generics, permissions
# Import models used in the API
from .models import User, Notification,Material
# Import serializers for each model
from .serializers import ResourceSerializer, UserSerializer,  NotificationSerializer
# Import ObtainAuthToken for token-based authentication
from rest_framework.authtoken.views import ObtainAuthToken
# Import Response for API responses
from rest_framework.response import Response
# Import status codes for API responses
from rest_framework import status
# Import FileResponse and Http404 for file downloads and error handling
from django.http import FileResponse, Http404
import os
# Import APIView for custom API endpoints
from rest_framework.views import APIView
# Import IsAuthenticated permission for endpoints requiring authentication
from rest_framework.permissions import IsAuthenticated
# Import timezone utilities
from django.utils import timezone
# Import Q for complex queries
from django.db.models import Q

# List all users (admin only)
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

# Retrieve a specific user (authenticated users)
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# List and create resources (authenticated or read-only)
class ResourceListCreateView(generics.ListCreateAPIView):
    queryset = Material.objects.all().order_by('-id') # type: ignore
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Save the resource; Material has no uploaded_by/subject fields
        resource = serializer.save()
        # Optional: notify students using derived subject name
        subject_name = None
        try:
            subject_name = resource.subtopic.topic.subject.name
        except Exception:
            subject_name = None
        for student in User.objects.filter(role='student'):
            Notification.objects.create(
                user=student,
                message=f"New resource uploaded: {resource.title}{f' ({subject_name})' if subject_name else ''}"
            )

# Register a new user
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        # Custom create to wrap response
        response = super().create(request, *args, **kwargs)
        return Response({'user': response.data}, status=status.HTTP_201_CREATED)

# Download a resource file (requires payment)

# Get or update the user's language
class UserLanguageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Return the user's current language
        return Response({'language': request.user.language})

    def patch(self, request):
        # Update the user's language
        language = request.data.get('language')
        if language not in dict(User.LANGUAGE_CHOICES):
            return Response({'detail': 'Invalid language.'}, status=400)
        request.user.language = language
        request.user.save()
        return Response({'language': request.user.language})

# List notifications for the user
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return notifications for the current user
        return Notification.objects.filter(user=self.request.user)  # type: ignore

# Mark a notification as read
class NotificationMarkReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, user=request.user)  # type: ignore
        except Notification.DoesNotExist:  # type: ignore
            return Response({'detail': 'Notification not found.'}, status=404)
        notification.read = True
        notification.save()
        return Response({'detail': 'Notification marked as read.'})



#
# Filter and list published materials based on search and filters
class FilteredMaterialsView(APIView):
    def get(self, request):
        queryset = Material.objects.all()
        search = request.GET.get('search')
        subject = request.GET.get('subject')
        grade = request.GET.get('grade')

        if search:
            queryset = queryset.filter(title__icontains=search)
        if subject:
            queryset = queryset.filter(subtopic__topic__subject__name=subject)
        if grade:
            queryset = queryset.filter(subtopic__topic__subject__grade=grade)
        queryset = queryset.order_by('order', 'id')
        serializer = ResourceSerializer(queryset, many=True)
        return Response(serializer.data)
         

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import (
    StudentProfile, StudentCourseProgress, StudentBadge,
    Activity, WeeklyActivity, StudentSkill, Event
)
from .serializers import (
    StudentProfileSerializer, CourseProgressSerializer,
    BadgeSerializer, ActivitySerializer, WeeklyActivitySerializer,
    SkillSerializer, EventSerializer
)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_data(request):
    """Fetch full dashboard data for logged-in student"""
    student = StudentProfile.objects.get(user=request.user)

    # Serialize data
    profile_data = StudentProfileSerializer(student).data
    courses_data = CourseProgressSerializer(StudentCourseProgress.objects.filter(student=student), many=True).data
    badges_data = BadgeSerializer(StudentBadge.objects.filter(student=student), many=True).data
    activity_data = ActivitySerializer(Activity.objects.filter(student=student).order_by("-timestamp")[:5], many=True).data
    weekly_data = WeeklyActivitySerializer(WeeklyActivity.objects.filter(student=student).order_by("date"), many=True).data
    skills_data = SkillSerializer(student.studentskill_set.all(), many=True).data
    events_data = EventSerializer(Event.objects.filter(student=student).order_by("date_time")[:5], many=True).data

    # Leaderboard (top 10 + student rank)
    leaderboard = StudentProfile.objects.order_by("-points")[:10].values("user__username", "points")
    rank = StudentProfile.objects.filter(points__gt=student.points).count() + 1

    return Response({
        "profile": profile_data,
        "courses": courses_data,
        "badges": badges_data,
        "recent_activity": activity_data,
        "weekly_activity": weekly_data,
        "skills": skills_data,
        "events": events_data,
        "leaderboard": list(leaderboard),
        "rank": rank
    })
