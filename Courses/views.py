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

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_detail.html', {'course': course})

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

    # Helper method to get course data from the session
    def get_course_from_session(self):
        course_data = self.request.session.get('course_data')  # Retrieve course data from the session
        if not course_data:
            raise ValueError("Course data not found in session. Please start the process again.")
        
        return course_data  # Return raw course data, no need for a MockCourse class


    # Step 1: Create Course Title
    @action(detail=False, methods=['get', 'post'], url_path='create-title', url_name='create-title')
    def create_course_title(self, request):
        if request.method == 'POST':
            form = CourseTitleForm(request.POST, request.FILES)  # Ensure request.FILES is passed
            if form.is_valid():
                course = form.save(commit=False)
                course.instructor = request.user
                course.save()
                request.session['course_id'] = course.id  # Store course ID in session for the next steps
                return redirect('courses-set-category')
            else:
                return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            form = CourseTitleForm()

        return render(request, 'course_title.html', {'form': form})


    # Step 2: Set Category
    @action(detail=False, methods=['get', 'post'], url_path='set-category', url_name='set-category')
    def set_category(self, request):
        course_data = self.get_course_from_session()  # Get session data (not a course model)
        if request.method == 'POST':
            form = CourseCategoryForm(request.POST)
            if form.is_valid():
                # Update session data with the category info
                course_data['category'] = form.cleaned_data['category']
                request.session['course_data'] = course_data  # Save updated data to session
                return redirect('courses-set-price')  # Go to the next step
        else:
            form = CourseCategoryForm()

        return render(request, 'course_category.html', {'form': form, 'course_data': course_data})

    # Step 3: Set Course Price
    @action(detail=False, methods=['get', 'post'])
    def set_price(self, request):
        course_data = self.get_course_from_session()  # Get session data (not a course model)
        if request.method == 'POST':
            form = CoursePriceForm(request.POST)
            if form.is_valid():
                # Update session data with price info as a string
                course_data['price'] = str(form.cleaned_data['price'])  # Convert Decimal to string
                request.session['course_data'] = course_data  # Save updated data to session
                return redirect('courses-add-lessons')  # Go to the next step
        else:
            form = CoursePriceForm()

        return render(request, 'course_price.html', {'form': form, 'course_data': course_data})


    # Step 4: Add Lessons
    @action(detail=False, methods=['get', 'post'])
    def add_lessons(self, request):
        course_data = self.get_course_from_session()  # Get session data (not a course model)
        if request.method == 'POST':
            form = LessonForm(request.POST, request.FILES)
            if form.is_valid():
                lesson = form.save(commit=False)
                
                # Retrieve the course ID from the session and fetch the actual course model
                course_id = request.session.get('course_id')  # Fetch the course ID from the session
                if course_id:
                    lesson.course = Course.objects.get(id=course_id)  # Fetch the actual course model using the ID
                    lesson.save()
                    return redirect('courses-review-course')  # Go to the review page
                else:
                    return redirect('courses-set-title')  # If no course ID in session, redirect to title step
        else:
            form = LessonForm()

        return render(request, 'upload_lesson.html', {'form': form, 'course_data': course_data})

    @action(detail=False, methods=['get', 'post'])
    def review_course(self, request):
        # Retrieve course ID from session
        course_id = request.session.get('course_id')  # Fetch course ID from session
        if not course_id:
            # If no course ID is found, redirect to the appropriate page (e.g., course title page)
            return redirect('courses-create-title')  # You can adjust this as per your flow

        # Fetch the actual course object from the database using the course_id
        course = Course.objects.get(id=course_id)
        
        # Get lessons related to this course
        lessons = course.lessons.all()

        if request.method == 'POST':
            return redirect('index')  # Redirect to the instructor dashboard

        return render(
            request,
            'course_review.html',
            {'course': course, 'lessons': lessons}
        )


class CourseListView(ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'

    # This will fetch all the courses, not filtering by instructor
    def get_queryset(self):
        return Course.objects.all()
