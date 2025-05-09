from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
from django.conf import settings

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=150)

    def __str__(self):
        return self.category_name

class Course(models.Model):
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')# create category model and assign relation
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    cover_video = CloudinaryField(resource_type="video", blank=True, null=True)
    cover_photo = CloudinaryField(resource_type="image", blank=True, null=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Video(models.Model):
    course = models.ForeignKey(Course, related_name="videos", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video_file = CloudinaryField(resource_type="video")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video_file = CloudinaryField(resource_type="video", blank=True, null=True)
    pdf_file = CloudinaryField(resource_type="raw", blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.title})"
    
    
class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(auto_now_add=True)
    progress_percentage = models.FloatField(default=0.0)  # Renamed from 'progress' to 'progress_percentage'

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"


class Progress(models.Model):
    enrollment = models.ForeignKey(
        Enrollment, on_delete=models.CASCADE, related_name='progress_entries'  # Changed related_name
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress')
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.enrollment.user.username} - {self.lesson.title} ({'Completed' if self.completed else 'Incomplete'})"


# class InstructorEarning(models.Model):
#     instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='earnings')
#     course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='earnings')
#     total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     last_updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.instructor.username} - {self.course.title}: ${self.total_earnings}"

class InstructorEarning(models.Model):
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='earnings')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='earnings')
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.instructor.username} - {self.course.title}: ${self.total_earnings}"