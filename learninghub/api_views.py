# Import Django REST Framework generic views and permissions
from rest_framework import generics, permissions
# Import models used in the API
from .models import Resource, User, Assignment, StudentProgress, ResourcePayment, Notification,AssignmentSubmission
# Import serializers for each model
from .serializers import ResourceSerializer, UserSerializer, AssignmentSerializer, StudentProgressSerializer, NotificationSerializer, AssignmentSubmissionSerializer
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
    queryset = Resource.objects.all().order_by('-created_at') # type: ignore
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

# List and create assignments (authenticated or read-only)
class AssignmentListCreateView(generics.ListCreateAPIView):
    queryset = Assignment.objects.all().order_by('-created_at')  # type: ignore
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Save the assignment and notify the assigned student
        assignment = serializer.save()
        Notification.objects.create(  # type: ignore
            user=assignment.assigned_to,
            message=f"New assignment: {assignment.title} (Due: {assignment.due_date.date()})"
        )

# List and create student progress records
class StudentProgressListCreateView(generics.ListCreateAPIView):
    queryset = StudentProgress.objects.all().order_by('-last_accessed')  # type: ignore
    serializer_class = StudentProgressSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# Retrieve, update, or delete a specific assignment
class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()  # type: ignore
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# Retrieve, update, or delete a specific student progress record
class StudentProgressDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentProgress.objects.all()  # type: ignore
    serializer_class = StudentProgressSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
class ResourceDownloadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            resource = Resource.objects.get(pk=pk)  # type: ignore
        except Resource.DoesNotExist:  # type: ignore
            raise Http404
        # Check if the user has paid for the resource
        has_paid = ResourcePayment.objects.filter(student=request.user, resource=resource, paid=True).exists()  # type: ignore
        if not has_paid:
            return Response({'detail': 'Payment required to download this resource.'}, status=403)
        file_path = resource.file.path
        if not os.path.exists(file_path):
            return Response({'detail': 'File not found.'}, status=404)
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))

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

# Confirm payment for a resource
class ConfirmResourcePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            payment = ResourcePayment.objects.get(student=request.user, resource_id=pk)  # type: ignore
        except ResourcePayment.DoesNotExist:  # type: ignore
            return Response({'detail': 'No payment record found.'}, status=404)
        payment.paid = True
        payment.save()
        Notification.objects.create(  # type: ignore
            user=request.user,
            message=f"Payment received. You can now download: {payment.resource.title}"
        )
        return Response({'detail': 'Payment confirmed. You can now download the resource.'})

# Student dashboard data (progress, assignments, activity, recommendations)
class StudentDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Progress per subject
        progress_qs = StudentProgress.objects.filter(user=user)  # type: ignore
        progress_per_subject = {}
        for p in progress_qs:
            subj = p.resource.subject
            if subj not in progress_per_subject or p.progress > progress_per_subject[subj]:
                progress_per_subject[subj] = p.progress
        progress_list = [
            {'subject': subj, 'progress': progress_per_subject[subj]}
            for subj in progress_per_subject
        ]
        # Upcoming assignments
        upcoming_assignments = Assignment.objects.filter(  # type: ignore
            assigned_to=user,
            due_date__gte=timezone.now(),
            status__in=['not_started', 'in_progress']
        ).order_by('due_date')
        upcoming = [
            {
                'id': a.id,
                'title': a.title,
                'due_date': a.due_date,
                'status': a.status
            } for a in upcoming_assignments
        ]
        # Recent activity (last 5 progress records)
        recent_activity = [
            {
                'resource': p.resource.title,
                'subject': p.resource.subject,
                'progress': p.progress,
                'last_accessed': p.last_accessed
            } for p in progress_qs.order_by('-last_accessed')[:5]
        ]
        # Recommendations (resources in most viewed subject, not yet viewed)
        if progress_per_subject:
            most_viewed_subject = max(progress_per_subject, key=progress_per_subject.get)  # type: ignore
            viewed_resource_ids = progress_qs.values_list('resource_id', flat=True)
            recommendations = Resource.objects.filter(  # type: ignore
                subject=most_viewed_subject
            ).exclude(id__in=viewed_resource_ids)[:5]
            recs = [
                {'id': r.id, 'title': r.title, 'subject': r.subject}
                for r in recommendations
            ]
        else:
            recs = []
        return Response({
            'progress_per_subject': progress_list,
            'upcoming_assignments': upcoming,
            'recent_activity': recent_activity,
            'recommendations': recs
        })

# Teacher dashboard data (uploaded resources, assignments, engagement)
class TeacherDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Uploaded resources
        uploaded_resources = Resource.objects.filter(uploaded_by=user)  # type: ignore
        resources_list = [
            {
                'id': r.id,
                'title': r.title,
                'subject': r.subject,
                'view_count': r.view_count,
                'download_count': r.download_count,
                'created_at': r.created_at
            } for r in uploaded_resources
        ]
        # Assignment submissions (assignments created by teacher)
        assignments = Assignment.objects.filter(resource__uploaded_by=user)  # type: ignore
        assignment_stats = [
            {
                'id': a.id,
                'title': a.title,
                'due_date': a.due_date,
                'assigned_to': str(a.assigned_to),
                'status': a.status,
                'grade': a.grade
            } for a in assignments
        ]
        # Student engagement (sum of views/downloads for teacher's resources)
        total_views = sum(r.view_count for r in uploaded_resources)
        total_downloads = sum(r.download_count for r in uploaded_resources)
        return Response({
            'uploaded_resources': resources_list,
            'assignment_submissions': assignment_stats,
            'student_engagement': {
                'total_views': total_views,
                'total_downloads': total_downloads
            }
        })

# List and create assignment submissions
class AssignmentSubmissionListCreateView(generics.ListCreateAPIView):
    queryset = AssignmentSubmission.objects.all().order_by('-submitted_at')  # type: ignore
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Save the submission and notify the student
        submission = serializer.save(student=self.request.user)
        Notification.objects.create(  # type: ignore
            user=submission.student,
            message=f"New assignment submission: {submission.assignment}"
        )

# Retrieve a specific assignment submission
class AssignmentSubmissionDetailView(generics.RetrieveAPIView):
    queryset = AssignmentSubmission.objects.all()  # type: ignore
    serializer_class = AssignmentSubmissionSerializer  # type: ignore
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'role') and user.role == 'student':
            return AssignmentSubmission.objects.filter(student=user)  # type: ignore
        return AssignmentSubmission.objects.all()  # type: ignore
        if user.role == 'student':
            return AssignmentSubmission.objects.filter(student=user)  # type: ignore
        return AssignmentSubmission.objects.all()  # type: ignore

# Activity feed for the user (recent notifications, resource views, submissions)
class ActivityFeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Recent notifications
        notifications = Notification.objects.filter(user=user).order_by('-created_at')[:5]  # type: ignore
        notifications_feed = [
            {
                'type': 'notification',
                'message': n.message,
                'created_at': n.created_at,
                'read': n.read
            } for n in notifications
        ]
        # Recent resource views
        progress = StudentProgress.objects.filter(user=user).order_by('-last_accessed')[:5]  # type: ignore
        resource_feed = [
            {
                'type': 'resource_view',
                'resource': p.resource.title,
                'subject': p.resource.subject,
                'progress': p.progress,
                'last_accessed': p.last_accessed
            } for p in progress
        ]
        # Recent assignment submissions
        submissions = AssignmentSubmission.objects.filter(student=user).order_by('-submitted_at')[:5]  # type: ignore
        submission_feed = [
            {
                'type': 'assignment_submission',
                'assignment': str(s.assignment),
                'status': s.status,
                'submitted_at': s.submitted_at,
                'grade': s.grade
            } for s in submissions
        ]
        # Combine and sort by date
        def get_sort_key(x):
            for key in ('created_at', 'last_accessed', 'submitted_at'):
                value = x.get(key)
                if value is not None:
                    return value
            # Fallback to a very old date if none found
            from datetime import datetime
            return datetime.min
        feed = notifications_feed + resource_feed + submission_feed
        feed.sort(key=get_sort_key, reverse=True)
        return Response({'activity_feed': feed})

# Provide dropdown options for materials (subjects, grades, types)
class MaterialDropdownOptionsView(APIView):
    def get(self, request):
        subjects = Resource.objects.values_list('subject', flat=True).distinct()#type: ignore
        grades = Resource.objects.values_list('grade', flat=True).distinct()#type: ignore
        # Get resource type choices from the model
        type_choices = [
            {"value": value, "label": label}
            for value, label in Resource.RESOURCE_TYPE_CHOICES
        ]
        return Response({
            "subjects": sorted([s for s in subjects if s]),
            "grades": sorted([g for g in grades if g]),
            "types": type_choices
        })

# Filter and list published materials based on search and filters
class FilteredMaterialsView(APIView):
    def get(self, request):
        queryset = Resource.objects.filter(status='published')#type: ignore
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
         