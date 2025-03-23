from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import User, EmployerProfile, JobSeekerProfile
from .forms import UserRegistrationForm, EmployerProfileForm, JobSeekerProfileForm
from jobs.models import JobPosting
from django.db.models import Q

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                user_type = form.cleaned_data.get('user_type')
                
                # Create corresponding profile based on user type
                if user_type == 'employer':
                    EmployerProfile.objects.create(user=user)
                else:
                    JobSeekerProfile.objects.create(user=user)
                
                # Log the user in
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=user.username, password=raw_password)
                login(request, user)
                
                # Redirect to complete profile
                if user_type == 'employer':
                    return redirect('complete_employer_profile')
                else:
                    return redirect('complete_job_seeker_profile')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

@login_required
def complete_employer_profile(request):
    """Complete employer profile after registration"""
    if not hasattr(request.user, 'employer_profile'):
        messages.error(request, "You don't have an employer profile.")
        return redirect('home')
    
    profile = request.user.employer_profile
    
    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('employer_dashboard')
    else:
        form = EmployerProfileForm(instance=profile)
    
    return render(request, 'complete_employer_profile.html', {'form': form})

@login_required
def complete_job_seeker_profile(request):
    """Complete job seeker profile after registration"""
    if not hasattr(request.user, 'job_seeker_profile'):
        messages.error(request, "You don't have a job seeker profile.")
        return redirect('home')
    
    profile = request.user.job_seeker_profile
    
    if request.method == 'POST':
        form = JobSeekerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('job_seeker_dashboard')
    else:
        form = JobSeekerProfileForm(instance=profile)
    
    return render(request, 'complete_job_seeker_profile.html', {'form': form})

@login_required
def employer_dashboard(request):
    """Dashboard for employers"""
    if not hasattr(request.user, 'employer_profile'):
        messages.error(request, "You don't have an employer profile.")
        return redirect('home')
    
    # Get employer's job postings
    jobs = request.user.employer_profile.job_postings.all().order_by('-created_at')
    
    # Get recent applications
    recent_applications = []
    for job in jobs:
        applications = job.applications.all().order_by('-applied_at')[:5]
        if applications:
            recent_applications.extend(applications)
    
    # Sort by applied_at date
    recent_applications = sorted(
        recent_applications, 
        key=lambda x: x.applied_at, 
        reverse=True
    )[:10]
    
    context = {
        'jobs': jobs,
        'recent_applications': recent_applications,
        'active_jobs_count': jobs.filter(is_active=True).count(),
        'total_applications_count': sum(job.applications.count() for job in jobs),
    }
    
    return render(request, 'employer_dashboard.html', context)

@login_required
def job_seeker_dashboard(request):
    """Dashboard for job seekers"""
    if not hasattr(request.user, 'job_seeker_profile'):
        messages.error(request, "You don't have a job seeker profile.")
        return redirect('home')
    
    # Get job seeker's applications
    applications = request.user.job_seeker_profile.applications.all().order_by('-applied_at')
    
    # Get recommended jobs based on skills and desired position
    profile = request.user.job_seeker_profile
    
    recommended_jobs = JobPosting.objects.filter(is_active=True).order_by('-created_at')
    
    # Filter by desired position if available
    if profile.desired_position:
        recommended_jobs = recommended_jobs.filter(
            Q(title__icontains=profile.desired_position) |
            Q(description__icontains=profile.desired_position)
        )
    
    # Filter by skills if available
    if profile.skills:
        skills = [s.strip() for s in profile.skills.split(',')]
        skill_query = Q()
        for skill in skills:
            skill_query |= Q(requirements__icontains=skill)
        recommended_jobs = recommended_jobs.filter(skill_query)
    
    # Filter by location if available
    if profile.desired_location:
        recommended_jobs = recommended_jobs.filter(
            Q(location__icontains=profile.desired_location) |
            Q(is_remote=True)
        )
    
    # Exclude jobs already applied to
    applied_job_ids = applications.values_list('job_id', flat=True)
    recommended_jobs = recommended_jobs.exclude(id__in=applied_job_ids)[:10]
    
    context = {
        'applications': applications[:10],
        'recommended_jobs': recommended_jobs,
        'applications_count': applications.count(),
    }
    
    return render(request, 'job_seeker_dashboard.html', context)

@login_required
def view_profile(request):
    """View current user's profile"""
    context = {}
    
    if hasattr(request.user, 'employer_profile'):
        context['profile'] = request.user.employer_profile
        context['profile_type'] = 'employer'
    elif hasattr(request.user, 'job_seeker_profile'):
        context['profile'] = request.user.job_seeker_profile
        context['profile_type'] = 'job_seeker'
    else:
        messages.error(request, "No profile found.")
        return redirect('home')
    
    return render(request, 'view_profile.html', context)



@login_required
def custom_logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect("home")
    return render(request, "logout_confirm.html")


