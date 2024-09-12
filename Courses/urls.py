from django.urls import include, path
from .views import instructor_dashboard
from rest_framework.routers import DefaultRouter

# from .views import CourseViewSet, CourseListView
from .views import CourseListView, CourseViewSet

router = DefaultRouter()

router.register(r"", CourseViewSet)

urlpatterns = [
    path('list', CourseListView.as_view(), name='course_list'),  # For rendering HTML using CBV
    path("instructor_dashboard", instructor_dashboard, name="instructor_dashboard"),
    path("api/courses/", include(router.urls)),
    path("courses/", CourseListView.as_view(), name="course_list"),
]

