from django.urls import path
from .views import home, create_admin


urlpatterns = [
    path('', home, name='home'),
    path('create-admin/', create_admin),
]