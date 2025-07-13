from rest_framework import serializers
from .models import User, Resource, Assignment, StudentProgress, ResourcePayment, Notification, AssignmentSubmission

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    language = serializers.ChoiceField(choices=User.LANGUAGE_CHOICES, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password', 'language']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user 

class ResourceSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    can_download = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = '__all__'

    def get_can_download(self, obj):
        user = self.context.get('request').user if self.context.get('request') else None  # type: ignore
        if not user or not getattr(user, 'is_authenticated', False):  # type: ignore
            return False
        return ResourcePayment.objects.filter(student=user, resource=obj, paid=True).exists()  # type: ignore

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

class StudentProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProgress
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentSubmission
        fields = '__all__'
