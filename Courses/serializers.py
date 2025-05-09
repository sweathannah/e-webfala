from rest_framework import serializers
from .models import Course, Lesson, Category

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.CharField(source='instructor.username', read_only=True) 
    cover_photo = serializers.SerializerMethodField() 

    def get_cover_photo(self, obj):
        if obj.cover_photo:
            return obj.cover_photo.url
        return "https://placehold.co/400x225" 

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructor', 'price', 'category', 'created_at', 'cover_photo']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'