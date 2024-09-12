from django.db import models
from django.conf import settings

# Create your models here.


class Course(models.Model):
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    ) 
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255, blank=True)  # create category model and assign relation
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, blank=True, null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    cover_video = models.FileField(upload_to="course_videos/", blank=True, null=True)
    cover_photo = models.ImageField(upload_to="course_covers/", blank=True, null=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Video(models.Model):
    course = models.ForeignKey(Course, related_name="videos", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to="videos/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to="lessons/videos/", blank=True, null=True)
    pdf_file = models.FileField(upload_to="lessons/pdfs/", blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.title})"
