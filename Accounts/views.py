
from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, InstructorProfileForm
from .models import UserProfile, InstructorProfile
from django.views import View
from django.contrib.auth.views import PasswordResetView
from dj_rest_auth.views import LogoutView
from django.conf import settings
import os

# Create your views here.



def custom_login_view(request):
    error_message = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            error_message = 'Invalid email or password'

    return render(request, 'accounts/login.html', {'error_message': error_message})


class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        """Handle GET request for logout to serve HTML."""
        if request.user.is_authenticated:
            self.logout(request)
        return render(request, "account/logout.html")


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.txt'
    html_email_template_name = 'registration/password_reset_email.html'
    
    
@login_required
def user_profile_form(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile(user = request.user)
        
    if request.method == 'POST':
        if 'profile_pic' in request.FILES:
            if profile.profile_pic:
                old_picture_path = os.path.join(settings.MEDIA_ROOT, str(profile.profile_pic))
                if os.path.isfile(old_picture_path):
                    os.remove(old_picture_path)

        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, "user_profile_form.html", {"form": form})


def instructor_profile_form(request):
    # Fetch or initialize the UserProfile
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    instructor_profile = InstructorProfile.objects.filter(user_profile=user_profile).first()
    
    # Initialize the form with existing data (if any)
    if instructor_profile:
        # Prepopulate the form with the existing instructor profile
        form = InstructorProfileForm(instance=instructor_profile)
    else:
        # Manually add user_profile data to initial form values
        initial_data = {
            "bio": user_profile.bio,
            "first_name": user_profile.first_name,
            "last_name": user_profile.last_name,
            "profile_pic": user_profile.profile_pic,
        }
        form = InstructorProfileForm(initial=initial_data)

    # Handle POST request
    if request.method == "POST":
        if instructor_profile:
            form = InstructorProfileForm(request.POST, request.FILES, instance=instructor_profile)
        else:
            form = InstructorProfileForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Save the form (creates or updates InstructorProfile)
            instructor_profile = form.save(commit=False)
            # Ensure the user_profile is linked correctly
            instructor_profile.user_profile = user_profile
            instructor_profile.save()
            print("Profile saved with data:", instructor_profile)  
            return redirect("instructor_profile")  # Redirect to a success page
        else:
            print("Form not valid. Errors:", form.errors)
    else:
        form = InstructorProfileForm(instance=instructor_profile)
        
    return render(request, "instructor_profile_form.html", {"form": form})

def instructor_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    instructor_profile = InstructorProfile.objects.filter(user_profile=user_profile).first()

    return render(request, "instructor_profile.html", {"user_profile": user_profile, "instructor_profile": instructor_profile})


def view_user_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)  # Get profile for the current user
    except UserProfile.DoesNotExist:
        profile = None  # Handle case where profile doesn't exist

    return render(request, 'userprofile.html', {'profile': profile})


