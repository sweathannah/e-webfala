from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import Course, Video, Lesson
from .form import (
    CourseTitleForm,
    CourseCategoryForm,
    VideoForm,
    CoursePriceForm,
    LessonForm,
)
from rest_framework import viewsets, permissions
from .serializers import CourseSerializer, LessonSerializer

# Create your views here.


def instructor_dashboard(request):
    courses = Course.objects.filter(
        instructor=request.user
    )  # Adjust this to fit your model
    return render(request, "instructur_dashboard.html", {"courses": courses})

class CourseListView(ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'  # Name for the context data to use in the template





# def course_create_title(request):
#     if request.method == 'POST':
#         form = CourseTitleForm(request.POST, request.FILES)
#         if form.is_valid():
#             course = form.save(commit=False)
#             course.instructor = request.user
#             course.save()
#             request.session['course_id'] = course.id  # Save course id to session for later steps
#             return redirect('course_create_category')  # Go to next step
#     else:
#         form = CourseTitleForm()

#     return render(request, 'course_title.html', {'form': form})

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

# def upload_lesson(request):
#     course_id = request.session.get('course_id')
#     course = Course.objects.get(id=course_id)

#     if request.method == 'POST':
#         form = LessonForm(request.POST, request.FILES)
#         if form.is_valid():
#             lesson = form.save(commit=False)
#             lesson.course = course
#             lesson.save()
#             return redirect('course_review')  # Redirect to course detail page
#     else:
#         form = LessonForm()

#     return render(request, 'upload_lesson.html', {'form': form, 'course': course})


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


# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]



class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Course.objects.all()

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

