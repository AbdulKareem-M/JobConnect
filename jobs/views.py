from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from .models import JobPosting, JobCategory, JobApplication
from .forms import JobPostingForm, JobApplicationForm
from accounts.models import EmployerProfile
from django.http import JsonResponse

def home(request):
    """Home page with featured job listings"""
    featured_jobs = JobPosting.objects.filter(is_active=True).order_by('-created_at')[:6]
    job_categories = JobCategory.objects.all()
    
    context = {
        'featured_jobs': featured_jobs,
        'job_categories': job_categories,
    }
    return render(request, 'home.html', context)

def job_listings(request):
    """Display all job listings with filtering options"""
    jobs = JobPosting.objects.filter(is_active=True).order_by('-created_at')
    categories = JobCategory.objects.all()
    
    # Filter by search query
    query = request.GET.get('q')
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(employer__company_name__icontains=query)
        )
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        jobs = jobs.filter(category_id=category_id)
    
    # Filter by job type
    job_type = request.GET.get('job_type')
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    
    # Filter by location
    location = request.GET.get('location')
    if location:
        jobs = jobs.filter(location__icontains=location)
    
    # Pagination
    paginator = Paginator(jobs, 10)  # 10 jobs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'jobs': page_obj,
        'categories': categories,
        'job_types': JobPosting.JOB_TYPE_CHOICES,
    }
    return render(request, 'job_listings.html', context)

def job_detail(request, job_id):
    """Display details for a specific job posting"""
    job = get_object_or_404(JobPosting, id=job_id, is_active=True)
    related_jobs = JobPosting.objects.filter(
        category=job.category, 
        is_active=True
    ).exclude(id=job_id)[:3]
    
    # Check if user has already applied
    has_applied = False
    if request.user.is_authenticated and hasattr(request.user, 'job_seeker_profile'):
        has_applied = JobApplication.objects.filter(
            job=job, 
            applicant=request.user.job_seeker_profile
        ).exists()
    
    context = {
        'job': job,
        'related_jobs': related_jobs,
        'has_applied': has_applied,
    }
    return render(request, 'job_detail.html', context)

@login_required
def post_job(request):
    # Check if user has an employer profile
    try:
        employer = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        messages.error(request, "You need an employer profile to post jobs.")
        return redirect('employer_dashboard')
    
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = employer
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect('employer_dashboard')
    else:
        form = JobPostingForm()
    
    return render(request, 'post_job.html', {'form': form})

@login_required
def apply_for_job(request, job_id):
    """Submit an application for a job"""
    job = get_object_or_404(JobPosting, id=job_id, is_active=True)
    
    # Check if user is a job seeker
    if not hasattr(request.user, 'job_seeker_profile'):
        messages.error(request, "Only job seekers can apply for jobs.")
        return redirect('job_detail', job_id=job.id)
    
    # Check if job is still accepting applications
    if job.is_expired():
        messages.error(request, "This job posting has expired.")
        return redirect('job_detail', job_id=job.id)
    
    # Check if user has already applied
    existing_application = JobApplication.objects.filter(
        job=job, 
        applicant=request.user.job_seeker_profile
    ).first()
    
    if existing_application:
        messages.info(request, "You have already applied for this job.")
        return redirect('view_application', application_id=existing_application.id)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user.job_seeker_profile
            
            # If user didn't upload a resume, use the one from their profile
            if not application.resume and request.user.job_seeker_profile.resume:
                application.resume = request.user.job_seeker_profile.resume
                
            application.save()
            messages.success(request, "Your application has been submitted!")
            return redirect('my_applications')
    else:
        form = JobApplicationForm()
    
    context = {
        'form': form,
        'job': job
    }
    return render(request, 'apply.html', context)

@login_required
def my_applications(request):
    """View all applications submitted by the current user"""
    if not hasattr(request.user, 'job_seeker_profile'):
        messages.error(request, "Only job seekers can view applications.")
        return redirect('home')
    
    applications = JobApplication.objects.filter(
        applicant=request.user.job_seeker_profile
    ).order_by('-applied_at')
    
    return render(request, 'my_applications.html', {'applications': applications})

@login_required
def view_application(request, application_id):
    """View details of a specific application"""
    # For job seekers
    if hasattr(request.user, 'job_seeker_profile'):
        application = get_object_or_404(
            JobApplication, 
            id=application_id, 
            applicant=request.user.job_seeker_profile
        )
    # For employers
    elif hasattr(request.user, 'employer_profile'):
        application = get_object_or_404(
            JobApplication, 
            id=application_id, 
            job__employer=request.user.employer_profile
        )
    else:
        messages.error(request, "You do not have permission to view this application.")
        return redirect('home')
    
    return render(request, 'view_application.html', {'application': application})

@login_required
def manage_jobs(request):
    """Manage jobs posted by the current employer"""
    if not hasattr(request.user, 'employer_profile'):
        messages.error(request, "Only employers can manage job postings.")
        return redirect('home')
    
    jobs = JobPosting.objects.filter(
        employer=request.user.employer_profile
    ).order_by('-created_at')
    
    return render(request, 'manage_jobs.html', {'jobs': jobs})

@login_required
def manage_applications(request, job_id):
    """Manage applications for a specific job"""
    if not hasattr(request.user, 'employer_profile'):
        messages.error(request, "Only employers can manage applications.")
        return redirect('home')
    
    job = get_object_or_404(
        JobPosting, 
        id=job_id, 
        employer=request.user.employer_profile
    )
    
    # Filter by status if provided
    status = request.GET.get('status')
    applications = job.applications.all().order_by('-applied_at')
    
    if status:
        applications = applications.filter(status=status)
    
    return render(request, 'manage_applications.html', {
        'job': job,
        'applications': applications,
        'status_choices': JobApplication.STATUS_CHOICES,
    })

@login_required
def update_application_status(request, application_id):
    if not hasattr(request.user, 'employer_profile'):
        messages.error(request, "Only employers can update application status.")
        return redirect('home')

    application = get_object_or_404(
        JobApplication, 
        id=application_id, 
        job__employer=request.user.employer_profile
    )

    if request.method == "POST":
        status = request.POST.get("status")
        valid_statuses = ["applied", "under_review", "shortlisted", "interview", "offered", "hired", "rejected"]

        if status in valid_statuses:
            application.status = status
            application.save()
            messages.success(request, f"Application status updated to {application.get_status_display()}.")
        else:
            messages.error(request, "Invalid status update.")

    return redirect("all_applications")




@login_required
def edit_job(request, job_id):
    """Edit an existing job posting"""
    if not hasattr(request.user, 'employer_profile'):
        messages.error(request, "Only employers can edit job postings.")
        return redirect('home')
    
    job = get_object_or_404(
        JobPosting, 
        id=job_id, 
        employer=request.user.employer_profile
    )
    
    if request.method == 'POST':
        form = JobPostingForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job posting updated successfully!")
            return redirect('manage_jobs')
    else:
        form = JobPostingForm(instance=job)
    
    return render(request, 'edit_job.html', {'form': form, 'job': job})


@login_required
def toggle_job_status(request, job_id):
    # Get the job posting object
    job = get_object_or_404(JobPosting, id=job_id)
    
    # Check if the user is the employer who posted this job
    if job.employer.user != request.user:
        messages.error(request, "You don't have permission to modify this job posting.")
        return redirect('employer_dashboard')
    
    # Toggle the status
    job.is_active = not job.is_active
    job.save()
    
    
    # For non-AJAX requests, redirect back with a message
    status_message = "activated" if job.is_active else "deactivated"
    messages.success(request, f"Job '{job.title}' has been {status_message}.")
    return redirect('employer_dashboard')


@login_required
def delete_job(request, job_id):
    """Delete an existing job posting"""
    if not hasattr(request.user, 'employer_profile'):
        messages.error(request, "Only employers can delete job postings.")
        return redirect('home')
    
    job = get_object_or_404(
        JobPosting, 
        id=job_id, 
        employer=request.user.employer_profile
    )
    
    if request.method == 'POST':
        # Store job title for confirmation message
        job_title = job.title
        # Delete the job
        job.delete()
        messages.success(request, f"Job '{job_title}' has been deleted successfully.")
        return redirect('manage_jobs')
    
    return render(request, 'delete_job.html', {'job': job})


@login_required
def applicant_details(request, application_id):
    """View details of a job applicant"""
    if not hasattr(request.user, 'employer_profile'):
        messages.error(request, "Only employers can view applicant details.")
        return redirect('home')
    
    # Get the application
    application = get_object_or_404(
        JobApplication, 
        id=application_id,
        job__employer=request.user.employer_profile
    )
    
    # Get the applicant profile
    applicant = application.applicant
    
    context = {
        'application': application,
        'applicant': applicant,
    }
    
    return render(request, 'applicant_details.html', context)

# In your views.py
@login_required
def all_applications(request):
    """View all applications for an employer"""
    if not hasattr(request.user, 'employer_profile'):
        messages.error(request, "You don't have employer privileges.")
        return redirect('home')
    
    # Get all applications for all jobs posted by this employer
    jobs = request.user.employer_profile.job_postings.all()
    applications = []
    
    for job in jobs:
        job_applications = job.applications.all()
        applications.extend(job_applications)
    
    # Sort applications by date
    applications = sorted(applications, key=lambda x: x.applied_at, reverse=True)
    
    return render(request, 'all_applications.html', {'applications': applications})