from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, instructor_dashboard, CourseListView

# Set up the router for the CourseViewSet
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
      # REST API routes
    path('', include(router.urls)),

    # View-based routes
    path('dashboard/', instructor_dashboard, name='index'),  # Changed to 'dashboard' for clarity
    path('courses/list/', CourseListView.as_view(), name='course_list'),
    path('courses/create-title/', CourseViewSet.as_view({'post': 'create_course_title'}), name='course-create-title'),
]
