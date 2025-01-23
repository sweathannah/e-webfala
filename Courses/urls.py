from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, instructor_dashboard, CourseListView, course_detail

# Set up the router for the CourseViewSet
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    # REST API routes
    path('api/', include(router.urls)),  # Change this to '/api/courses' or another prefix

    # View-based routes
    path('dashboard/', instructor_dashboard, name='index'),
    path('courses/<int:course_id>/', course_detail, name='course_detail'),
    path('courses/list/', CourseListView.as_view(), name='course_list'),  # This will render the list page
    path('courses/create-title/', CourseViewSet.as_view({'post': 'create_course_title','get': 'create_course_title'}), name='course-create-title'),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)