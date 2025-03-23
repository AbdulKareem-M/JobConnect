from django import forms
from .models import JobPosting, JobApplication, JobCategory

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        exclude = ['employer', 'created_at', 'updated_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'requirements': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'responsibilities': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'experience_level': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'salary_min': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minimum salary'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Maximum salary'}),
            'is_remote': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'application_deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['cover_letter', 'resume']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'rows': 5, 
                'placeholder': 'Write a cover letter explaining why you are a good fit for this position...'
            }),
        }

class JobSearchForm(forms.Form):
    query = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Job title, keywords, or company name'
    }))
    category = forms.ModelChoiceField(
        queryset=JobCategory.objects.all(),
        required=False,
        empty_label="All Categories"
    )
    job_type = forms.ChoiceField(
        choices=[('', 'All Types')] + list(JobPosting.JOB_TYPE_CHOICES),
        required=False
    )
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'City, state, or "Remote"'
    }))