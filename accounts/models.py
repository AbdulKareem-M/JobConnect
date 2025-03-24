from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('employer', 'Employer'),
        ('job_seeker', 'Job Seeker'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    email = models.EmailField(_('email address'), unique=True)
    
    # Fix the reverse accessor clashes by adding related_name
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='accounts_user_set',
        related_query_name='accounts_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='accounts_user_set',
        related_query_name='accounts_user',
    )

    def is_employer(self):
        return self.user_type == 'employer'
    
    def is_job_seeker(self):
        return self.user_type == 'job_seeker'


class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=100)
    company_description = models.TextField()
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    industry = models.CharField(max_length=50)
    company_website = models.URLField(blank=True)
    company_location = models.CharField(max_length=100)
    company_size = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.company_name

class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='job_seeker_profile')
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    education = models.TextField(blank=True)
    desired_position = models.CharField(max_length=100, blank=True)
    desired_location = models.CharField(max_length=100, blank=True)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user}"