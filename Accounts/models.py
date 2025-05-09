from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from Courses.models import Course
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Custom user manager where email is the unique identifiers for authentication instead of usernames."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with the given email and password."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    username = None

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete= models.CASCADE)
    profile_pic = models.ImageField(upload_to="profile_image", blank=True, null=True)
    first_name = models.CharField(max_length=20, null=False, blank=False)
    last_name = models.CharField(max_length=20, null=False, blank=False)
    bio = models.TextField(max_length=255, null=False, blank=False)
    courses_registered = models.ManyToManyField(Course)
    
    def __str__(self):
        return f"UserProfile for {self.user.email}"
    
    
class InstructorProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    profile_pic = models.ImageField(upload_to="profile_image", blank=True, null=True)
    first_name = models.CharField(max_length=20, null=False, blank=False)
    last_name = models.CharField(max_length=20, null=False, blank=False)
    bio = models.TextField(
        max_length=500,
        null=False,
        blank=False,
        help_text="Include your specialization, qualifications, and teaching experience."
    )
    cv = models.FileField(
        upload_to="instructor_cv's",
        null=False,
        blank=False,
        help_text="Upload your CV."
    )
    courses_to_take = models.TextField(
        null=False,
        blank=False,
        help_text="List the courses you want to teach, separated by commas."
    )
    AVAILABILITY_CHOICES = [
        ('full_time', 'Full-Time'),
        ('part_time', 'Part-Time'),
        ('other', 'Other'),
    ]
    availability = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default='full_time',
        help_text="Select your teaching availability."
    )
    other_availability_details = models.TextField(
        max_length=255,
        null=True,
        blank=True,
        help_text="If 'Other' is selected, provide details here."
    )
    teaching_experience = models.BooleanField(
        default=False,
        help_text="Do you have prior teaching experience?"
    )

    def __str__(self):
        # Fetch names from UserProfile
        return f"{self.user_profile.first_name} {self.user_profile.last_name}"

