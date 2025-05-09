from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('profile_form/', views.user_profile_form, name ="user_profile_form"),
    path('instructor_profile_form', views.instructor_profile_form, name="instructor_profile_form"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = 'registration/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name = 'registration/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'registration/password_reset_complete.html'), name='password_reset_complete'),
    # path('custom-password-reset/', views.CustomPasswordResetView.as_view(), name='custom_password_reset'),
    path('account/logout', views.CustomLogoutView.as_view(), name='account_logout'),
    path('user_profile/', views.view_user_profile, name='user_profile'),
    path('instructor_profile/', views.instructor_view, name='instructor_profile')
    
    
]

