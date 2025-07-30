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
        # Save the resource and notify all students
        resource = serializer.save(uploaded_by=self.request.user)
        students = User.objects.filter(role='student')  # type: ignore
        for student in students:
            Notification.objects.create(  # type: ignore
                user=student,
                message=f"New resource uploaded: {resource.title} ({resource.subject})"
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
        queryset = Material.objects.filter(status='published')#type: ignore
        search = request.GET.get('search')
        subject = request.GET.get('subject')
        grade = request.GET.get('grade')
        resource_type = request.GET.get('type')
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if subject:
            queryset = queryset.filter(subject=subject)
        if grade:
            queryset = queryset.filter(grade=grade)
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)
        queryset = queryset.order_by('-created_at')
        serializer = ResourceSerializer(queryset, many=True)
        return Response(serializer.data)
         