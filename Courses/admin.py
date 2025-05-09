
from django.contrib import admin
from .models import Category, Course, Lesson, Video

# Register your models here.

admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Lesson)
admin.site.register(Video)
