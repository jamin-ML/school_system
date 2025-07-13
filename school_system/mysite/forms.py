from django import forms
from .models import Materials,TeacherResource

class MaterialUploadForm(forms.ModelForm):
    class Meta:
        model = Materials
        fields = ['title', 'description', 'file', 'video_file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'video_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
class ResourceUploadForm(forms.ModelForm):
    class Meta:
        model = TeacherResource
        fields = ['title','resource_type', 'file', 'subject', 'grade_level','content_body']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'resource_type': forms.Select(attrs={'class': 'form-control'}),
        }