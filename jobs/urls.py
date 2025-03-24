from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('jobs/', views.job_listings, name='job_listings'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/post/', views.post_job, name='post_job'),
    path('jobs/<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('jobs/<int:job_id>/apply/', views.apply_for_job, name='apply_for_job'),
    path('applications/', views.my_applications, name='my_applications'),
    path('applications/<int:application_id>/', views.view_application, name='view_application'),
    path('application/<int:application_id>/update/<str:status>/', views.update_application_status, name='update_application_status'),
    path('manage/jobs/', views.manage_jobs, name='manage_jobs'),
    path('manage/jobs/<int:job_id>/applications/', views.manage_applications, name='manage_applications'),
    path('jobs/<int:job_id>/toggle-status/', views.toggle_job_status, name='toggle_job_status'),
    path('jobs/<int:job_id>/delete/', views.delete_job, name='delete_job'),
    path('applications/<int:application_id>/applicant/', views.applicant_details, name='applicant_details'),
    path('applications/all/', views.all_applications, name='all_applications'),
]

    