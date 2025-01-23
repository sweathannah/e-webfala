from django.contrib import admin
from .models import CustomUser

# Register your models here.


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "is_student", "is_instructor", "date_joined")


admin.site.register(CustomUser, CustomUserAdmin)
