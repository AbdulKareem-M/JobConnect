from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path("logout/", views.custom_logout_view, name="logout"),
    
    
    # Profile URLs
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/employer/complete/', views.complete_employer_profile, name='complete_employer_profile'),
    path('profile/job-seeker/complete/', views.complete_job_seeker_profile, name='complete_job_seeker_profile'),
    
    # Dashboard URLs
    path('dashboard/employer/', views.employer_dashboard, name='employer_dashboard'),
    path('dashboard/job-seeker/', views.job_seeker_dashboard, name='job_seeker_dashboard'),
        
]