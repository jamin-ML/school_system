# Import Django's forms module for creating forms
from django import forms
# Import Django's built-in user creation form
from django.contrib.auth.forms import UserCreationForm
# Import the custom User model
from .models import User
 
# Custom user creation form extending Django's UserCreationForm
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # Use the custom User model
        model = User
        # Include all default fields plus 'role' and 'language'
        fields = UserCreationForm.Meta.fields + ('role', 'language') 