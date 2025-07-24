# Import Django REST Framework's serializer base classes
from rest_framework import serializers
# Import models to be serialized
from .models import User, Resource, Assignment, StudentProgress, ResourcePayment, Notification, AssignmentSubmission

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
    # Add a computed field to indicate if the resource is HTML content
    is_html = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = ['id', 'title', 'subject', 'grade', 'resource_type', 'description', 'file', 'is_html']

    def get_is_html(self, obj):
        # Return True if the resource is HTML content only
        return obj.is_html

# Serializer for the Assignment model
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'  # Serialize all fields

# Serializer for the StudentProgress model
class StudentProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProgress
        fields = '__all__'  # Serialize all fields

# Serializer for the Notification model
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'  # Serialize all fields

# Serializer for the AssignmentSubmission model
class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentSubmission
        fields = '__all__'  # Serialize all fields
