from django.urls import include, path
from .views import instructor_dashboard
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet,CourseListView

router = DefaultRouter()

router.register(r"", CourseViewSet)

urlpatterns = [
    path('list', CourseListView.as_view(), name='course_list'),  # For rendering HTML using CBV
    path("instructor_dashboard", instructor_dashboard, name="instructor_dashboard"),
    path("", include(router.urls)),
]
