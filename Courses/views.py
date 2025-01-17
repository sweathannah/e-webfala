from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from rest_framework.decorators import action
from .models import Course, Video, Lesson
from .form import (
    CourseTitleForm,
    CourseCategoryForm,
    VideoForm,
    CoursePriceForm,
    LessonForm,
)
from django.views.generic import TemplateView
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CourseSerializer, LessonSerializer

# Create your views here.

@login_required
def instructor_dashboard(request):
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'instructur_dashboard.html', {'courses': courses})

class CourseListView(ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Course.objects.all()

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

    # Step 1: Create Course Title
    @action(detail=False, methods=['get', 'post'], url_path='create-title', url_name='create-title')
    def create_course_title(self, request):
        if request.method == 'POST':
            form = CourseTitleForm(request.POST or None)
            if form.is_valid():
                course = form.save(commit=False)
                course.instructor = request.user
                course.save()
                request.session['course_id'] = course.id  # Store course ID for the next steps
                return redirect('courses-set-category')   # Go to the next step
            else:
                return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            form = CourseTitleForm()

        return render(request, 'course_title.html', {'form': form})

    @action(detail=False, methods=['get', 'post'], url_path='set-category', url_name='set-category')
    def set_category(self, request):
        course = self.get_course_from_session()
        if request.method == 'POST':
            form = CourseCategoryForm(request.POST, instance=course)
            if form.is_valid():
                form.save()
                return redirect('courses-set-price')  # Go to the next step
        else:
            form = CourseCategoryForm(instance=course)

        return render(request, 'course_category.html', {'form': form, 'course': course})



    # Step 3: Set Course Price
    @action(detail=False, methods=['get', 'post'])
    def set_price(self, request):
        course = self.get_course_from_session()
        if request.method == 'POST':
            form = CoursePriceForm(request.POST, instance=course)
            if form.is_valid():
                form.save()
                return redirect('courses-add-lessons')  # Go to the next step
        else:
            form = CoursePriceForm(instance=course)

        return render(request, 'course_price.html', {'form': form, 'course': course})

    # Step 4: Add Lessons
    @action(detail=False, methods=['get', 'post'])
    def add_lessons(self, request):
        course = self.get_course_from_session()
        if request.method == 'POST':
            form = LessonForm(request.POST, request.FILES)
            if form.is_valid():
                lesson = form.save(commit=False)
                lesson.course = course
                lesson.save()
                return redirect('courses-review-course')  # Go to the review page
        else:
            form = LessonForm()

        return render(request, 'upload_lesson.html', {'form': form, 'course': course})

    # Step 5: Review Course and Submit
    @action(detail=False, methods=['get', 'post'])
    def review_course(self, request):
        course = self.get_course_from_session()
        lessons = course.lessons.all()

        if request.method == 'POST':
            # Finalize course creation
            return redirect('index')  # Redirect to the instructor dashboard

        return render(
            request,
            'course_review.html',
            {'course': course, 'lessons': lessons}
        )


    # Helper method to get course object from session
    def get_course_from_session(self):
        course_id = self.request.session.get('course_id')
        return get_object_or_404(Course, id=course_id)
    


class CourseListView(TemplateView):
    template_name = "course_list.html"



