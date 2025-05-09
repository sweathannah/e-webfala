from django.contrib import admin
from .models import CustomUser, UserProfile

# Register your models here.


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "password", "username", "is_student", "is_instructor", "date_joined")

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "bio")
    
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(UserProfile, UserProfileAdmin)
