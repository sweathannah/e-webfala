from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView


router = DefaultRouter()


schema_view = get_schema_view(
    openapi.Info(
        title="Udemy Clone API",
        default_version="v1",
        description="API documentation for the Udemy clone",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("", include("allauth.urls")),
    path("api/register/", RegisterView.as_view(), name="rest_register"),
    path("api/login/", LoginView.as_view(), name="rest_login"),
    path("api/logout/", LogoutView.as_view(), name="rest_logout"),
    path("api/user/", UserDetailsView.as_view(), name="rest_user_details"),
    path("admin/", admin.site.urls),
    path("", include("home.urls"), name="home"),
    path("payments/", include("payments.urls")),
    path("", include("Courses.urls"), name="courses"),
    path("__reload__/", include("django_browser_reload.urls")),
    path("api/", include(router.urls)),
]

# Add this section to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
