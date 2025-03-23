# admin.py
from django.contrib import admin
from .models import JobCategory, JobPosting

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'category', 'job_type', 'is_active', 'application_deadline')
    list_filter = ('is_active', 'job_type', 'category', 'experience_level')
    search_fields = ('title', 'description')