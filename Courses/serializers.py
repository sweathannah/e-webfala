from rest_framework import serializers
from .models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.CharField(source='instructor.username', read_only=True) 

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructor', 'price', 'category', 'created_at']

