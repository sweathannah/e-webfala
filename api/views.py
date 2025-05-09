from django.shortcuts import render
from Courses.models import Course, Category
from Courses.serializers import CourseSerializer, CategorySerializer
from rest_framework import generics

# Create your views here.

class CourseListView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
