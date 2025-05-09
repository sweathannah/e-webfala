from django.urls import include, path
from .views import instructor_dashboard, create_checkout_session, enrolled_courses, course_progress, user_courses
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, CategoryViewSet, CategoryListView, CourseListView

# from .views import CourseViewSet, CourseListView
# from .views import CourseListView, CourseViewSet

router = DefaultRouter()

router.register(r"courses", CourseViewSet)
router.register(r"categories", CategoryViewSet)

urlpatterns = [
    path("instructor_dashboard", instructor_dashboard, name="instructor_dashboard"),
    path("categories", CategoryListView.as_view(template_name = "categories.html"), name = 'category_list'),
    path("api/", include(router.urls)),
    path("api/courses/", include(router.urls)),
    path("courses/", CourseListView.as_view(), name="course_list"),
    path('create-checkout-session/<int:course_id>/', create_checkout_session, name='create_checkout_session'),
    path('dashboard/', enrolled_courses, name='dashboard'),
    path('progress/<int:course_id>/', course_progress, name='course_progress'),
    path('my-courses/', user_courses, name='user_courses'),
]

