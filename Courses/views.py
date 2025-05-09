from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Video, Lesson, Category, Enrollment, Progress, InstructorEarning
from .form import (
    CourseTitleForm,
    CourseCategoryForm,
    VideoForm,
    CoursePriceForm,
    LessonForm,
)
from django.views.generic import TemplateView
from rest_framework import viewsets, permissions
from .serializers import CourseSerializer, CategorySerializer
from django.views.generic import ListView
import stripe
from django.http import JsonResponse
from decimal import Decimal

# Create your views here.

def instructor_dashboard(request):
    courses = Course.objects.filter(
        instructor=request.user
    )  # Adjust this to fit your model
    return render(request, "instructur_dashboard.html", {"courses": courses})


def course_create_title(request):
    if request.method == 'POST':
        form = CourseTitleForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            request.session['course_id'] = course.id  # Save course id to session for later steps
            return redirect('course_create_category')  # Go to next step
    else:
        form = CourseTitleForm()

    return render(request, 'course_title.html', {'form': form})

def create_checkout_session(request, course_id):
    course = Course.objects.get(id=course_id)

    # Create a Checkout session
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': course.title,
                    'description': course.description,
                },
                'unit_amount': int(course.price * 100),  # Stripe expects the price in cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(f'/payments/success/?course_id={course_id}'),
        cancel_url=request.build_absolute_uri('/payments/cancel/'),
    )

    return JsonResponse({
        'id': checkout_session.id
    })

# Handle video upload for course
def course_video_create(request, course_id):
    course = Course.objects.get(id=course_id)

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.course = course
            video.save()
            return redirect('course_detail', course_id=course.id)  # Redirect after save
    else:
        form = VideoForm()

    return render(request, 'course_video_create.html', {'form': form})

def enroll_in_course(request, course_id):
    if request.method == "POST":
        user = request.user  # Authenticated user
        course = get_object_or_404(Course, id=course_id)

        # Check if the user is already enrolled
        if Enrollment.objects.filter(user=user, course=course).exists():
            return JsonResponse({"message": "You are already enrolled in this course."}, status=400)

        # Create enrollment
        Enrollment.objects.create(user=user, course=course)
        return JsonResponse({"message": "Enrollment successful!"}, status=200)

    return JsonResponse({"error": "Invalid request method."}, status=405)

def enrolled_courses(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect unauthenticated users to login

    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
    return render(request, 'dashboard.html', {'enrollments': enrollments})

# def course_progress(request, enrollment_id):
#     enrollment = get_object_or_404(Enrollment, id=enrollment_id, user=request.user)
#     progress = Progress.objects.filter(enrollment=enrollment).select_related('section')

#     total_lessons = enrollment.course.lessons.count()
#     completed_sections = progress.filter(completed=True).count()
#     progress_percentage = (completed_sections / total_lessons) * 100 if total_lessons > 0 else 0

#     enrollment.progress = progress_percentage
#     enrollment.save()

#     return render(request, 'course_progress.html', {
#         'enrollment': enrollment,
#         'progress': progress,
#         'progress_percentage': progress_percentage
#     })

def calculate_earnings(course, sale_amount, commission_rate=0.1):
    """
    Calculate earnings for the instructor based on a sale.
    :param course: Course object.
    :param sale_amount: Total sale amount for the course.
    :param commission_rate: Percentage of the sale retained by the platform.
    :return: Earnings for the instructor.
    """
    instructor_share = Decimal(1) - Decimal(commission_rate)
    earning = sale_amount * instructor_share

    # Update or create earnings record for the instructor
    earning_record, created = InstructorEarning.objects.get_or_create(
        instructor=course.instructor,
        course=course,
    )
    earning_record.total_earnings += earning
    earning_record.save()
    return earning

def course_progress(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment = get_object_or_404(Enrollment, course=course, user=request.user)

    lessons = course.lessons.all()  # Use 'lessons' instead of 'sections'
    progress_data = []

    for lesson in lessons:
        progress_entry, created = Progress.objects.get_or_create(
            enrollment=enrollment, lesson=lesson
        )
        progress_data.append({
            'lesson_title': lesson.title,
            'completed': progress_entry.completed,
        })

    return render(request, 'course_progress.html', {
        'course': course,
        'progress_data': progress_data,
        'progress_percentage': enrollment.progress_percentage,
    })

def user_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
    
    courses_data = []
    for enrollment in enrollments:
        course = enrollment.course
        lessons = course.lessons.all()
        videos = course.videos.all()
        
        courses_data.append({
            'course': course,
            'progress': enrollment.progress_percentage,  # Updated field
            'lessons': lessons,
            'videos': videos,
        })
    
    return render(request, 'user_courses.html', {
        'courses_data': courses_data,
    })


# # Step 2: Category
# def course_create_category(request):
#     course_id = request.session.get('course_id')
#     course = Course.objects.get(id=course_id)

#     if request.method == 'POST':
#         form = CourseCategoryForm(request.POST, instance=course)
#         if form.is_valid():
#             form.save()
#             return redirect('course_create_price')
#     else:
#         form = CourseCategoryForm(instance=course)

#     return render(request, 'course_category.html', {'form': form})

# # Step 3: Price
# def course_create_price(request):
#     course_id = request.session.get('course_id')
#     course = Course.objects.get(id=course_id)

#     if request.method == 'POST':
#         form = CoursePriceForm(request.POST, instance=course)
#         if form.is_valid():
#             form.save()
#             return redirect('course_create_lessons')
#     else:
#         form = CoursePriceForm(instance=course)

#     return render(request, 'course_price.html', {'form': form})

def upload_lesson(request):
    course_id = request.session.get('course_id')
    course = Course.objects.get(id=course_id)

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect('course_review')  # Redirect to course detail page
    else:
        form = LessonForm()

    return render(request, 'upload_lesson.html', {'form': form, 'course': course})


# # Step 5: Review and Submit
# def course_review(request):
#     course_id = request.session.get('course_id')
#     course = Course.objects.get(id=course_id)
#     videos = Video.objects.filter(course=course)
#     lessons = course.lessons.all()

#     if request.method == 'POST':
#         # Finalize course creation and redirect to the course list or detail page
#         return redirect('course_list')

#     return render(request, 'course_review.html', {'course': course, 'videos': videos, 'lessons': lessons})


# def course_list(request):
#     courses = Course.objects.all()  # Retrieve all courses from the database
#     return render(request, 'course_list.html', {'courses': courses})


# def course_detail(request, course_id):
#     course = get_object_or_404(Course, id=course_id)
#     lessons = course.lessons.all()  # Assuming Course has a reverse relation to Lesson
#     return render(request, 'course_detail.html', {'course': course, 'lessons': lessons})


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()
    
class CategoryListView(TemplateView):
    template_name = 'categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.prefetch_related('courses').all()  # Fetch all categories
        return context



class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Course.objects.all()
    
        category = self.request.query_params.get('category', None)
        minimum_price = self.request.query_params.get('minimum_price', None)
        maximum_price = self.request.query_params.get('maximum_price', None)

        if category:
            queryset = queryset.filter(category_name=category)

        if minimum_price and maximum_price:
            queryset = queryset.filter(price_greaterthan=minimum_price, price_lessthan=maximum_price)

        return queryset
    


    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)


class CourseListView(TemplateView):
    template_name = "course_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = Course.objects.all()

        category = self.request.GET.get('category', None)
        minimum_price = self.request.GET.get('minimum_price', None)
        maximum_price = self.request.GET.get('maximum_price', None)

        if category:
            queryset = queryset.filter(category_name=category)

        if minimum_price and maximum_price:
            queryset = queryset.filter(price_greaterthan=minimum_price, price_lessthan=maximum_price)

        context['courses'] = queryset
        context['categories'] = Category.objects.all()

        return context
    
