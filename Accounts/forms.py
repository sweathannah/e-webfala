from django import forms
from .models import UserProfile, InstructorProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'first_name', 'last_name', 'bio'] 
        
class InstructorProfileForm(forms.ModelForm):
    # first_name = forms.CharField(required=True)
    # last_name = forms.CharField(required=True)
    # profile_pic = forms.ImageField(required=False)
    # bio = forms.CharField(widget=forms.Textarea, required=True)
    class Meta:
        model = InstructorProfile
        fields = ['bio', 'cv', 'courses_to_take', 'availability', 'other_availability_details', 'teaching_experience', 'first_name', 'last_name', 'profile_pic']
