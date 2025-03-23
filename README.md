# JobConnect

JobConnect is a job portal built with Django that allows employers to post jobs and job seekers to find and apply for jobs. It features a user authentication system, job management, and application tracking.

## Features

### **Authentication & User Profiles**
- User registration and login (Django built-in authentication)
- Employer and job seeker profiles
- Profile completion for better job matching

### **Job Management**
- Employers can post, edit, and delete jobs
- Job seekers can browse job listings and view details
- Employers can toggle job visibility (active/inactive)

### **Application System**
- Job seekers can apply for jobs
- Employers can review applications and manage candidates
- Applicants can track their submitted applications
- Employers can update application statuses

### **Dashboard**
- Separate dashboards for employers and job seekers
- Employers can manage job postings and view applications
- Job seekers can track their applications

### **Upcoming Features**
- Messaging system for direct communication between employers and job seekers

## Tech Stack
- **Backend:** Django, Python
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite/MySQL
- **Authentication:** Django built-in auth system

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/jobconnect.git
   cd jobconnect
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   - Open `http://127.0.0.1:8000/` in your browser.

## Usage

- **Employers**: Register, complete their profile, post jobs, manage applications.
- **Job Seekers**: Register, complete their profile, browse jobs, apply for jobs.

## URLs

### **Accounts App**
- `register/` - User Registration
- `login/` - User Login
- `logout/` - Logout
- `profile/` - View Profile
- `profile/employer/complete/` - Complete Employer Profile
- `profile/job-seeker/complete/` - Complete Job Seeker Profile
- `dashboard/employer/` - Employer Dashboard
- `dashboard/job-seeker/` - Job Seeker Dashboard

### **Jobs App**
- `/` - Home
- `jobs/` - Job Listings
- `jobs/<job_id>/` - Job Detail View
- `jobs/post/` - Post a New Job
- `jobs/<job_id>/edit/` - Edit Job Posting
- `jobs/<job_id>/apply/` - Apply for a Job
- `applications/` - View User Applications
- `applications/<application_id>/` - View Specific Application
- `manage/jobs/` - Employer Job Management
- `manage/jobs/<job_id>/applications/` - Manage Applications for a Job

## Screenshots

### Home Page
screenshots/home.png

### Application Detail
screenshots/application_detail.png

### Applications Page
screenshots/applications.png

### Complete Job Seeker Profile
screenshots/complete_job_seeker_profile.png

### Employer Dashboard
screenshots/dashboard_employer.png

### Job Seeker Dashboard
screenshots/dashboard_job_seeker.png

### Job Detail View
screenshots/job_detail.png

### Job Listings Page
screenshots/jobs.png

### Registration Page
screenshots/register.png

## Contributors
- **[Abdul Kareem]** - Developer

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---
Feel free to modify the project as needed!

