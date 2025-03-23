from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, EmployerProfile, JobSeekerProfile
class UserRegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        widget=forms.RadioSelect(),
        required=True,
        help_text='select if you are an employer or job-seeker'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type')
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'user_type', 'password1', 'password2']

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        exclude = ['user']
        widgets = {
            'company_description': forms.Textarea(attrs={'rows': 5}),
        }

class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        exclude = ['user']
        widgets = {
            'skills': forms.TextInput(attrs={
                'placeholder': 'Enter skills separated by commas (e.g., Python, Django, JavaScript)'
            }),
            'education': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Enter your education history'
            }),
        }