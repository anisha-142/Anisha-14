from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import re
from django.utils import timezone
from django.utils.html import strip_tags
from django.conf import settings
from placement_app.models import Student, PlacementOfficer, Company, College, JobRequirement, JobApplication, Notification, InterviewRound, InterviewResult, PracticeAttempt
from django.core.mail import send_mail
from django.template.loader import render_to_string


# LANDING PAGE
def index(request):
    return render(request, "index.html")

def logout_view(request):
    logout(request)
    return redirect('index')

# LOGIN VIEW
# def loginpage(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
            
#             # SMTP Email: Send Successful Login Alert
#             if user.email:
#                 try:
#                     send_mail(
#                         subject='Login Alert - JSS Campus Placement Portal',
#                         message=f'Hello {user.username},\n\nYou have successfully logged in to your account on the JSS Campus Placement Portal. Thank you and welcome!\n\nIf this was not you, please contact support immediately.',
#                         from_email=settings.DEFAULT_FROM_EMAIL,
#                         recipient_list=[user.email],
#                         fail_silently=True,
#                     )
#                 except Exception as e:
#                     pass

#             next_url = request.GET.get('next')
#             if next_url:
#                 return redirect(next_url)
            
#             if user.is_superuser or user.is_staff or hasattr(user, 'placementofficer'):
#                 return redirect('placementhome')
                
#             if Company.objects.filter(user=user).exists():
#                 return redirect('company_home')
#             return redirect('home')
#         else:
#             messages.error(request, 'Invalid username or password. Please try again.')
#             return redirect('login')
#     return render(request, 'login.html')

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from placement_app.models import Company, PlacementOfficer, UserProfile
from django.http import JsonResponse
import random
import string

def generate_captcha():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

def refresh_captcha(request):
    captcha = generate_captcha()
    request.session['captcha'] = captcha
    return JsonResponse({'captcha': captcha})

def loginpage(request):
    if request.method == "POST":
        user_captcha = request.POST.get("captcha", "")
        expected_captcha = request.session.get("captcha", "")
        
        if not expected_captcha or user_captcha.upper() != expected_captcha:
            messages.error(request, 'Invalid CAPTCHA. Please try again.')
            return redirect('login')

        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Get user role from UserProfile
            user_role = None
            if hasattr(user, 'userprofile'):
                user_role = user.userprofile.role
            
            # SMTP Email: Send Successful Login Alert
            if user.email:
                try:
                    # Customized email based on user role
                    role_name = "Admin"
                    if user_role == "COMPANY":
                        role_name = "Company Representative"
                    elif user_role == "STUDENT":
                        role_name = "Student"
                    
                    send_mail(
                        subject=f'Login Alert - JSS Campus Placement Portal ({role_name})',
                        message=f"""
                        Hello {user.username},

                        You have successfully logged in to your {role_name} account on the JSS Campus Placement Portal.

                        Login Details:
                        • Time: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
                        • Role: {role_name}

                        If this was you, you can safely ignore this email.
                        If this was not you, please contact support immediately at placement@jss.edu.in

                        Thank you for using JSS Campus Placement Portal!
                        """,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=True,
                    )
                except Exception as e:
                    # Log error but don't break login flow
                    print(f"Email sending failed: {e}")
                    pass

            # Handle next URL parameter
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            
            # Role-based redirection logic
            # 1. Superuser / Staff / Placement Officer
            if user.is_superuser or user.is_staff or hasattr(user, 'placementofficer'):
                return redirect('placementhome')
            
            # 2. Company User
            if hasattr(user, 'company') or Company.objects.filter(user=user).exists():
                # Fetch company details for welcome message
                company = Company.objects.get(user=user)
                messages.success(request, f'Welcome back to {company.name}!')
                return redirect('company_home')
            
            # 3. Student User
            if hasattr(user, 'student') or Student.objects.filter(user=user).exists():
                return redirect('student_home')  # or 'home' as per your URL name
            
            # 4. Fallback for generic users
            return redirect('home')
            
        else:
            # Authentication failed
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect('login')
    
    # GET request - display login page
    captcha = generate_captcha()
    request.session['captcha'] = captcha
    return render(request, 'login.html', {'captcha': captcha})
# FORGOT PASSWORD VIEW
# views.py

import random

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings


def forgot_password(request):

    if request.method == "POST":

        step = request.POST.get("step")

        # STEP 1 → SEND OTP
        if step == "send_otp":

            email = request.POST.get("email")

            try:
                user = User.objects.get(email=email)

                otp = random.randint(100000, 999999)

                request.session['reset_email'] = email
                request.session['reset_otp'] = str(otp)

                send_mail(
                    subject='Password Reset OTP',
                    message=f'Your OTP for password reset is: {otp}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False,
                )

                messages.success(request, "OTP sent to your email.")

                return render(request, 'forgot_password.html', {
                    'show_otp': True,
                    'email': email
                })

            except User.DoesNotExist:
                messages.error(request, "No account found with this email.")

        # STEP 2 → VERIFY OTP & RESET PASSWORD
        elif step == "verify_otp":

            entered_otp = request.POST.get("otp")
            new_password = request.POST.get("new_password")

            session_otp = request.session.get("reset_otp")
            email = request.session.get("reset_email")

            if entered_otp == session_otp:

                user = User.objects.get(email=email)

                user.password = make_password(new_password)
                user.save()

                del request.session['reset_otp']
                del request.session['reset_email']

                messages.success(request, "Password reset successful.")

                return redirect('login')

            else:
                messages.error(request, "Invalid OTP.")

                return render(request, 'forgot_password.html', {
                    'show_otp': True,
                    'email': email
                })

    return render(request, 'forgot_password.html')

# REGISTER VIEW (REVERTED TO SIMPLE)
# def register(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         # Validation
#         if not re.match(r'^[A-Za-z]+$', username):
#             messages.error(request, "Username should contain only letters.")
#             return redirect('register')

#         password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$'
#         if not re.match(password_pattern, password):
#             messages.error(request, "Password must contain uppercase, lowercase, number, special character and minimum 8 characters.")
#             return redirect('register')

#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists")
#             return redirect('register')

#         try:
#             user = User.objects.create_user(
#                 username=username,
#                 email=email,
#                 password=password
#             )
#             user.save()

#             # SMTP Email: Send Welcome Email
#             try:
#                 subject = "Welcome to My Website"
#                 html_message = render_to_string("emails/welcome_email.html", {
#                     "name": username,
#                     "email": email
#                 })
#                 plain_message = strip_tags(html_message)

#                 send_mail(
#                     subject,
#                     plain_message,
#                     settings.DEFAULT_FROM_EMAIL,
#                     [email],
#                     html_message=html_message,
#                     fail_silently=False
#                 )
#             except Exception as e:
#                 print("Email error:", e)

#             messages.success(request, f"Registration Successful! Welcome {username}. Please Login.")
#             return redirect('login')
#         except Exception as e:
#             messages.error(request, f"Error during registration: {str(e)}")
#             return redirect('register')

#     return render(request, "register.html")
# views.py
import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.db import transaction
from placement_app.models import UserProfile, Student, College

def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Student-specific fields
        registration_number = request.POST.get("registration_number")
        college_id = request.POST.get("college")
        department = request.POST.get("department")
        course = request.POST.get("course")
        year = request.POST.get("year")
        cgpa = request.POST.get("cgpa")
        percentage_10th = request.POST.get("percentage_10th")
        percentage_12th = request.POST.get("percentage_12th")
        backlogs = request.POST.get("backlogs", 0)

        # Validation
        if not re.match(r'^[A-Za-z]+$', username):
            messages.error(request, "Username should contain only letters.")
            return redirect('register')

        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$'
        if not re.match(password_pattern, password):
            messages.error(request, "Password must contain uppercase, lowercase, number, special character and minimum 8 characters.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')
        
        if Student.objects.filter(registration_number=registration_number).exists():
            messages.error(request, "Registration number already exists")
            return redirect('register')

        try:
            with transaction.atomic():
                # Create User
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=request.POST.get("first_name", ""),
                    last_name=request.POST.get("last_name", "")
                )
                
                # Create UserProfile with STUDENT role
                UserProfile.objects.create(
                    user=user,
                    role="STUDENT"
                )
                
                # Get College
                college = College.objects.get(id=college_id)
                
                # Create Student profile
                student = Student.objects.create(
                    user=user,
                    college=college,
                    registration_number=registration_number,
                    department=department,
                    course=course,
                    year=int(year),
                    cgpa=float(cgpa),
                    percentage_10th=float(percentage_10th),
                    percentage_12th=float(percentage_12th),
                    backlogs=int(backlogs) if backlogs else 0
                )

                # Send Welcome Email
                try:
                    subject = "Welcome to JSS Placement Portal"
                    html_message = render_to_string("emails/welcome_email.html", {
                        "name": username,
                        "email": email,
                        "registration_number": registration_number,
                        "role": "Student"
                    })
                    plain_message = strip_tags(html_message)

                    send_mail(
                        subject,
                        plain_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        html_message=html_message,
                        fail_silently=False
                    )
                except Exception as e:
                    print("Email error:", e)

                messages.success(request, f"Registration Successful! Welcome {username}. Please Login to complete your profile.")
                return redirect('login')
                
        except College.DoesNotExist:
            messages.error(request, "Selected college does not exist")
            return redirect('register')
        except Exception as e:
            messages.error(request, f"Error during registration: {str(e)}")
            return redirect('register')

    # GET request - get all colleges for dropdown
    colleges = College.objects.all().order_by('name')
    return render(request, "register.html", {'colleges': colleges})
# HOME PAGE AFTER LOGIN
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from placement_app.models import Student, Company, JobRequirement, JobApplication, InterviewResult, Notification

@login_required(login_url='login')
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    try:
        student = Student.objects.get(user=request.user)
        my_apps = JobApplication.objects.filter(student=student)
        total_applied = my_apps.count()
        total_shortlisted = my_apps.filter(status='Shortlisted').count()
        total_selected = my_apps.filter(status='Selected').count()
        
        # Recommendation logic
        search_query = request.GET.get('q', '')
        applied_job_ids = my_apps.values_list('job_id', flat=True)
        
        # Don't slice before filtering
        recommended_jobs_qs = JobRequirement.objects.exclude(id__in=applied_job_ids).select_related('company')
        
        if search_query:
            recommended_jobs_qs = recommended_jobs_qs.filter(
                Q(title__icontains=search_query) |
                Q(company__name__icontains=search_query)
            )
        
        # Apply slice at the very end
        recommended_jobs_qs = recommended_jobs_qs.order_by('-created_at')[:10]

        # ── ELIGIBILITY & DEADLINE URGENCY per job ──────────────────────────
        from datetime import date as _date
        today = _date.today()
        student_dept = (student.department or '').strip().lower()

        recommended_jobs = []
        eligible_count = 0
        for job in recommended_jobs_qs:
            cgpa_ok = (student.cgpa or 0) >= (job.min_cgpa or 0)
            backlog_ok = (student.backlogs or 0) <= (job.max_backlogs if job.max_backlogs is not None else 99)
            dept_list = [d.strip().lower() for d in (job.eligible_departments or '').split(',')]
            dept_ok = (not dept_list) or any(d and d in student_dept or student_dept in d for d in dept_list)
            is_eligible = cgpa_ok and backlog_ok and dept_ok

            days_left = (job.deadline - today).days if job.deadline else None
            if days_left is None:
                deadline_label, deadline_class = 'No deadline', 'deadline-normal'
            elif days_left < 0:
                deadline_label, deadline_class = 'Expired', 'deadline-expired'
            elif days_left == 0:
                deadline_label, deadline_class = '⚡ Closes Today!', 'deadline-today'
            elif days_left == 1:
                deadline_label, deadline_class = '⏰ Closes Tomorrow', 'deadline-tomorrow'
            elif days_left <= 5:
                deadline_label, deadline_class = f'⏱ {days_left} days left', 'deadline-soon'
            else:
                deadline_label, deadline_class = f'{days_left} days left', 'deadline-normal'

            if is_eligible:
                eligible_count += 1

            recommended_jobs.append({
                'job': job,
                'is_eligible': is_eligible,
                'days_left': days_left,
                'deadline_label': deadline_label,
                'deadline_class': deadline_class,
            })

        recommended_jobs_count = eligible_count
        # ─────────────────────────────────────────────────────────────────────
        
        # PLACEMENT PROGRESS LOGIC
        # 1. Profile Completeness (based on 8 key fields)
        profile_fields = [
            student.registration_number, 
            student.department, 
            student.course, 
            student.year, 
            student.cgpa, 
            student.percentage_10th, 
            student.percentage_12th, 
            student.resume
        ]
        filled_fields = sum(1 for f in profile_fields if f)
        profile_completeness = int((filled_fields / len(profile_fields)) * 100)
        
        # 2. Practice Score (based on actual practice attempts, default to base calculation)
        attempts = PracticeAttempt.objects.filter(student=student)
        if attempts.exists():
            total_score = sum(a.score for a in attempts)
            total_possible = sum(a.total_questions for a in attempts)
            practice_score = int((total_score / total_possible) * 100)
        else:
            practice_score = int((student.cgpa / 10 * 70)) if student.cgpa else 60
            
        if practice_score > 100: practice_score = 100
        if practice_score < 30: practice_score = 30
        
        # 3. Interview Readiness (based on quiz completion, job applications, and cleared interview rounds)
        results = InterviewResult.objects.filter(application__student=student)
        cleared_rounds = results.filter(result='Cleared').count()
        
        unique_categories = attempts.values_list('category', flat=True).distinct().count()
        practice_bonus = min(30, unique_categories * 6)  # max +30% for completing categories
        app_bonus = min(15, total_applied * 5)  # max +15% for applications
        interview_bonus = min(15, cleared_rounds * 10)  # max +15% for cleared rounds
        
        interview_readiness = 40 + practice_bonus + app_bonus + interview_bonus
        if interview_readiness > 100: interview_readiness = 100

        
        # 4. Notifications
        notifications = Notification.objects.filter(
            Q(student=student) | Q(student__isnull=True)
        ).order_by('-created_at')[:5]
        
        unread_notifications_count = Notification.objects.filter(
            Q(student=student) | Q(student__isnull=True), 
            is_read=False
        ).count()
        
        import os
        from django.conf import settings
        resources_dir = os.path.join(settings.BASE_DIR, 'campusplacement')
        template_resources = []
        if os.path.exists(resources_dir):
            for f in os.listdir(resources_dir):
                f_lower = f.lower()
                if f_lower.endswith(('.pdf', '.pptx', '.ppt', '.docx', '.doc', '.txt')):
                    if f_lower.endswith('.pdf'):
                        icon = 'fa-file-pdf'
                        color = 'text-red-500'
                        bg_color = 'bg-red-50'
                        file_type = 'PDF Document'
                        file_type_class = 'pdf'
                    elif f_lower.endswith(('.pptx', '.ppt')):
                        icon = 'fa-file-powerpoint'
                        color = 'text-orange-500'
                        bg_color = 'bg-orange-50'
                        file_type = 'Presentation'
                        file_type_class = 'presentation'
                    elif f_lower.endswith('.txt'):
                        icon = 'fa-file-alt'
                        color = 'text-slate-500'
                        bg_color = 'bg-slate-50'
                        file_type = 'Text Notes'
                        file_type_class = 'word'
                    else:
                        icon = 'fa-file-word'
                        color = 'text-blue-500'
                        bg_color = 'bg-blue-50'
                        file_type = 'Word Document'
                        file_type_class = 'word'
                    template_resources.append({
                        'name': f,
                        'icon': icon,
                        'color': color,
                        'bg_color': bg_color,
                        'file_type': file_type,
                        'file_type_class': file_type_class
                    })
        
        context = {
            'student': student,
            'total_applied': total_applied,
            'total_shortlisted': total_shortlisted,
            'total_selected': total_selected,
            'recommended_jobs': recommended_jobs,
            'recommended_jobs_count': recommended_jobs_count,
            'notifications': notifications,
            'unread_notifications_count': unread_notifications_count,
            'profile_completeness': profile_completeness,
            'interview_readiness': interview_readiness,
            'practice_score': practice_score,
            'search_query': search_query,
            'template_resources': template_resources[:8],
        }
        return render(request, "student/home.html", context)
        
    except Student.DoesNotExist:
        if Company.objects.filter(user=request.user).exists():
            return redirect('company_home')
        
        # For non-student users
        context = {
            'student': None, 
            'total_applied': 0, 
            'total_shortlisted': 0, 
            'total_selected': 0,
            'recommended_jobs': [],
            'notifications': [],
            'unread_notifications_count': 0,
            'profile_completeness': 0,
            'interview_readiness': 0,
            'practice_score': 0,
            'search_query': '',
        }
        return render(request, "student/home.html", context)

def generate_resume(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return redirect('login')
        
    target_role     = request.GET.get('role', 'Professional')
    custom_skills   = request.GET.get('skills', '')
    custom_project  = request.GET.get('project', '')
    custom_summary  = request.GET.get('summary', '')
    custom_experience = request.GET.get('experience', '')
    custom_education  = request.GET.get('education', '')
    custom_awards   = request.GET.get('awards', '')
    custom_backlogs = request.GET.get('backlogs', '0')
    
    # Split skills if provided
    skills_list = [s.strip() for s in custom_skills.split(',') if s.strip()]
    
    context = {
        'student':            student,
        'target_role':        target_role,
        'custom_skills':      skills_list,
        'custom_project':     custom_project,
        'custom_summary':     custom_summary,
        'custom_experience':  custom_experience,
        'custom_education':   custom_education,
        'custom_awards':      custom_awards,
        'custom_backlogs':    custom_backlogs,
    }
    
    return render(request, "student/resume_template.html", context)

# ─── COMPANY LOGIN ────────────────────────────────────────────────────────
def company_login(request):
    """
    Dedicated login for Company users.
    Only users who have an associated Company profile are allowed in.
    Non-company users see: "Access denied: कंपनी उपयोगकर्ता नहीं है"
    """
    # Already logged-in company user → straight to dashboard
    if request.user.is_authenticated and Company.objects.filter(user=request.user).exists():
        return redirect('company_home')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Role check – only users with a Company profile
            if Company.objects.filter(user=user).exists():
                login(request, user)
                return redirect('company_home')
            else:
                # Deny non-company users with the required Hindi message
                messages.error(
                    request,
                    "Access denied: कंपनी उपयोगकर्ता नहीं है"
                )
        else:
            messages.error(request, "Invalid username or password. Please try again.")

        return redirect('company_login')

    # Auto-create test company user for demonstration if none exist
    if not User.objects.filter(username="testcompany").exists():
        test_user = User.objects.create_user(username="testcompany", email="test@company.com", password="Company@123")
        Company.objects.create(
            user=test_user, 
            name="TCS (Test Company)", 
            hr_name="HR Manager", 
            hr_email="test@company.com", 
            hr_phone="9876543210", 
            description="Auto-generated test company"
        )
        messages.info(request, "A test company has been created automatically. Username: testcompany | Password: Company@123")

    return render(request, 'company/company_login.html')


def company_home(request):
    if not request.user.is_authenticated:
        return redirect('company_login')
        
    try:
        company = Company.objects.get(user=request.user)
        active_jobs = JobRequirement.objects.filter(company=company)
        active_jobs_count = active_jobs.count()
        
        job_ids = active_jobs.values_list('id', flat=True)
        total_applicants = JobApplication.objects.filter(job_id__in=job_ids).count()
        shortlisted_count = JobApplication.objects.filter(job_id__in=job_ids, status='Shortlisted').count()
        pending_reviews = JobApplication.objects.filter(job_id__in=job_ids, status='Applied').count()
        selected_count = JobApplication.objects.filter(job_id__in=job_ids, status='Selected').count()
        rejected_count = JobApplication.objects.filter(job_id__in=job_ids, status='Rejected').count()
        
        recent_applications = JobApplication.objects.filter(job_id__in=job_ids).order_by('-id')[:5]
        
        upcoming_rounds = InterviewRound.objects.filter(job_id__in=job_ids, scheduled_date__gte=timezone.now()).order_by('scheduled_date')[:5]
        
        context = {
            'company': company,
            'active_jobs': active_jobs,
            'active_jobs_count': active_jobs_count,
            'total_applicants': total_applicants,
            'shortlisted_count': shortlisted_count,
            'pending_reviews': pending_reviews,
            'selected_count': selected_count,
            'rejected_count': rejected_count,
            'upcoming_rounds': upcoming_rounds,
            'recent_applications': recent_applications,
        }
        return render(request, "company/company_dashboard.html", context)
    except Company.DoesNotExist:
        # Not a company user – deny access and show an error
        messages.error(request, "Access denied: कंपनी उपयोगकर्ता नहीं है")
        return redirect('company_login')

def company_post_job(request):
    if not request.user.is_authenticated:
        return redirect('company_login')
    
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        messages.error(request, "Access denied.")
        return redirect('company_login')
        
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        package = request.POST.get('package')
        job_type = request.POST.get('job_type')
        min_cgpa = request.POST.get('min_cgpa')
        max_backlogs = request.POST.get('max_backlogs')
        eligible_departments = request.POST.get('eligible_departments')
        deadline = request.POST.get('deadline')
        
        try:
            JobRequirement.objects.create(
                company=company,
                title=title,
                description=description,
                location=location,
                package=package,
                job_type=job_type,
                min_cgpa=float(min_cgpa or 0.0),
                max_backlogs=int(max_backlogs or 0),
                eligible_departments=eligible_departments,
                deadline=deadline
            )
            messages.success(request, f"Successfully posted new job: {title}")
            return redirect('company_home')
        except Exception as e:
            messages.error(request, f"Error posting job: {str(e)}")
            
    return render(request, "company/post_job.html", {'company': company})

def company_applications(request):
    if not request.user.is_authenticated:
        return redirect('company_login')
        
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        messages.error(request, "Access denied.")
        return redirect('company_login')
        
    if request.method == "POST":
        app_id = request.POST.get('application_id')
        new_status = request.POST.get('status')
        try:
            application = JobApplication.objects.get(id=app_id, job__company=company)
            application.status = new_status
            application.save()
            messages.success(request, f"Successfully updated application status to {new_status}")
        except Exception as e:
            messages.error(request, "Error updating status")
            
        return redirect('company_applications')
        
    # Get all applications for jobs posted by this company
    applications = JobApplication.objects.filter(job__company=company).order_by('-applied_at')
    
    context = {
        'company': company,
        'applications': applications
    }
    return render(request, "company/applications.html", context)

def company_interviews(request):
    if not request.user.is_authenticated:
        return redirect('company_login')
        
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        messages.error(request, "Access denied.")
        return redirect('company_login')
    
    # Get all jobs for this company
    jobs = JobRequirement.objects.filter(company=company)
    
    # Get all interviews for this company's jobs
    interviews = InterviewRound.objects.filter(
        job__company=company
    ).order_by('-scheduled_date')
    
    if request.method == "POST":
        job_id = request.POST.get('job_id')
        round_name = request.POST.get('round_name')
        round_type = request.POST.get('round_type')
        date = request.POST.get('scheduled_date')
        time_val = request.POST.get('scheduled_time')
        description = request.POST.get('description')
        
        try:
            job = JobRequirement.objects.get(id=job_id, company=company)
            
            # Combine date and time
            from datetime import datetime
            dt_str = f"{date} {time_val}"
            scheduled_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
            
            # Create interview round with correct field names from your model
            interview_round = InterviewRound.objects.create(
                job=job,
                name=round_name,  # Use 'name' field from your model
                round_type=round_type,  # Use 'round_type' field
                scheduled_date=scheduled_dt,
                # Note: Your model doesn't have description field
                # If you want to store description, you need to add it to the model
            )
            
            # If you have a description field in your model, uncomment this:
            # interview_round.description = description
            # interview_round.save()
            
            messages.success(request, f"Successfully scheduled {round_name} for {job.title}")
            
        except JobRequirement.DoesNotExist:
            messages.error(request, "Selected job does not exist")
        except Exception as e:
            messages.error(request, f"Error scheduling interview: {str(e)}")
            
        return redirect('company_interviews')
    
    context = {
        'company': company,
        'jobs': jobs,
        'interviews': interviews,
    }
    return render(request, 'company/interviews.html', context)
        
    jobs = JobRequirement.objects.filter(company=company)
    interviews = InterviewRound.objects.filter(job__in=jobs).order_by('scheduled_date')
    
    context = {
        'company': company,
        'jobs': jobs,
        'interviews': interviews
    }
    return render(request, "company/interviews.html", context)

def company_profile(request):
    if not request.user.is_authenticated:
        return redirect('company_login')
        
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        messages.error(request, "Access denied.")
        return redirect('company_login')
        
    if request.method == "POST":
        company.name = request.POST.get('name')
        company.website = request.POST.get('website')
        company.description = request.POST.get('description')
        company.hr_name = request.POST.get('hr_name')
        company.hr_email = request.POST.get('hr_email')
        company.hr_phone = request.POST.get('hr_phone')
        
        try:
            company.save()
            messages.success(request, "Profile updated successfully!")
        except Exception as e:
            messages.error(request, f"Error updating profile: {str(e)}")
            
        return redirect('company_profile')
        
    return render(request, "company/profile.html", {'company': company})

# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
import json
from placement_app.models import Company, JobRequirement, JobApplication, Student

@login_required(login_url='login')
def companies(request):
    # Get the logged-in student
    try:
        student = Student.objects.get(user=request.user)
        applied_job_ids = list(JobApplication.objects.filter(
            student=student
        ).values_list('job_id', flat=True))
    except Student.DoesNotExist:
        student = None
        applied_job_ids = []
    
    # Get search query
    search_query = request.GET.get('q', '')
    
    # Get all companies that have job requirements
    companies_qs = Company.objects.filter(
        jobrequirement__isnull=False
    ).distinct()
    
    if search_query:
        companies_qs = companies_qs.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Prepare company data with their jobs
    company_data = []
    for company in companies_qs:
        jobs = JobRequirement.objects.filter(
            company=company,
            deadline__gte=timezone.now().date()  # Only active jobs
        ).order_by('-created_at')
        
        jobs_list = []
        for job in jobs:
            jobs_list.append({
                'id': job.id,
                'title': job.title,
                'job_type': job.job_type,
                'package': job.package,
                'location': job.location,
                'deadline': job.deadline.strftime('%Y-%m-%d'),
                'min_cgpa': float(job.min_cgpa) if job.min_cgpa else 0,
                'max_backlogs': job.max_backlogs,
                'eligible_departments': job.eligible_departments.split(',') if job.eligible_departments else [],
                'is_applied': job.id in applied_job_ids,
            })
        
        if jobs_list:  # Only show companies with active jobs
            company_data.append({
                'id': company.id,
                'name': company.name,
                'description': company.description,
                'website': company.website or '',
                'hr_name': company.hr_name,
                'hr_email': company.hr_email,
                'hr_phone': company.hr_phone,
                'jobs': jobs_list,
                'total_jobs': len(jobs_list)
            })
    
    context = {
        'companies': json.dumps(company_data, cls=DjangoJSONEncoder),
        'total_companies': len(company_data),
        'search_query': search_query,
    }
    
    return render(request, "student/companies.html", context)


# views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
import json
from placement_app.models import Company, JobRequirement, JobApplication, Student, Notification, UserProfile

@login_required(login_url='login')
@require_http_methods(["POST"])
def apply_job_ajax(request):
    """Handle job application via AJAX"""
    try:
        # Check if it's an AJAX request
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'Invalid request type'
            }, status=400)
        
        # Parse JSON data
        try:
            data = json.loads(request.body)
            job_id = data.get('job_id')
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON data'
            }, status=400)
        
        if not job_id:
            return JsonResponse({
                'success': False,
                'message': 'Job ID is required'
            }, status=400)
        
        # Get the student profile
        try:
            student = Student.objects.select_related('user', 'college').get(user=request.user)
        except Student.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Student profile not found. Please complete your profile first.'
            }, status=400)
        
        # Get the job
        try:
            job = JobRequirement.objects.select_related('company').get(id=job_id)
        except JobRequirement.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Job posting not found'
            }, status=404)
        
        # Check if already applied
        if JobApplication.objects.filter(student=student, job=job).exists():
            return JsonResponse({
                'success': False,
                'message': 'You have already applied for this position'
            }, status=400)
        
        # Check deadline
        if job.deadline < timezone.now().date():
            return JsonResponse({
                'success': False,
                'message': f'Application deadline has passed (Deadline: {job.deadline})'
            }, status=400)
        
        # Check CGPA requirement
        if job.min_cgpa and student.cgpa < job.min_cgpa:
            return JsonResponse({
                'success': False,
                'message': f'CGPA requirement not met. Required: {job.min_cgpa}, Your CGPA: {student.cgpa}'
            }, status=400)
        
        # Check backlog requirement
        if job.max_backlogs and student.backlogs > job.max_backlogs:
            return JsonResponse({
                'success': False,
                'message': f'Backlog limit exceeded. Max allowed: {job.max_backlogs}, Your backlogs: {student.backlogs}'
            }, status=400)
        
        # Check department eligibility
        if job.eligible_departments and job.eligible_departments.strip():
            eligible_depts = [d.strip().lower() for d in job.eligible_departments.split(',')]
            if student.department.lower() not in eligible_depts:
                return JsonResponse({
                    'success': False,
                    'message': f'Your department ({student.department}) is not eligible for this position. Eligible: {job.eligible_departments}'
                }, status=400)
        
        # Create application
        application = JobApplication.objects.create(
            student=student,
            job=job,
            status='Applied'
        )
        
        # Create notification
        Notification.objects.create(
            student=student,
            message=f'You have successfully applied for "{job.title}" at {job.company.name}. Good luck!',
            is_read=False
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Successfully applied for {job.title} at {job.company.name}!'
        })
        
    except Exception as e:
        # Log the error (you can add proper logging here)
        print(f"Error in apply_job_ajax: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return JsonResponse({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }, status=500)

def apply_job(request):
    try:
        student = Student.objects.get(user=request.user)
    except:
        student = None
        
    if request.method == "POST" and student:
        job_id = request.POST.get("job_id")
        if job_id:
            try:
                job = JobRequirement.objects.get(id=job_id)
                if not JobApplication.objects.filter(student=student, job=job).exists():
                    JobApplication.objects.create(student=student, job=job, status="Applied")
            except JobRequirement.DoesNotExist:
                pass
        return redirect('applications')
        
    jobs = JobRequirement.objects.all()
    return render(request, "student/apply_job.html", {"jobs": jobs})

def applications(request):
    try:
        student = Student.objects.get(user=request.user)
        apps = JobApplication.objects.filter(student=student).select_related(
            'job', 'job__company'
        ).order_by('-applied_at')
        total_applied = apps.count()
        total_shortlisted = apps.filter(status='Shortlisted').count()
        total_selected = apps.filter(status='Selected').count()
        total_rejected = apps.filter(status='Rejected').count()
    except Student.DoesNotExist:
        apps = []
        total_applied = 0
        total_shortlisted = 0
        total_selected = 0
        total_rejected = 0

    context = {
        'applications': apps,
        'total_applied': total_applied,
        'total_shortlisted': total_shortlisted,
        'total_selected': total_selected,
        'total_rejected': total_rejected,
    }
    return render(request, "student/applications.html", context)

def resources(request):
    if not request.user.is_authenticated:
        messages.info(request, "Login Required: Study resources are only available to registered students. Please login first.")
        return redirect('/login/?next=/resources/')
        
    import os
    from django.conf import settings
    resources_dir = os.path.join(settings.BASE_DIR, 'campusplacement')
    template_resources = []
    
    # Subject categories grouping structure
    subjects_map = {
        'C Programming': [],
        'Python Programming': [],
        'PHP Programming': [],
        'Data Structures & Algorithms': [],
        'Database Management (DBMS)': [],
        'AI & Data Science': [],
        'Operating Systems & Linux': [],
        'Web Technology': [],
        'Digital Marketing': [],
        'Computer Architecture (CMA)': [],
        'Mathematics & Discrete Structures': [],
        'General / Other Materials': []
    }
    
    def classify_file(filename):
        name = filename.lower()
        import re
        # Normalise underscores & hyphens to spaces so keywords like
        # 'artificial intelligence' match 'Artificial_Intelligence_...' files
        name_clean = name.replace('_', ' ').replace('-', ' ')

        if 'php' in name:
            return 'PHP Programming'
        elif (any(k in name_clean for k in [
                'data science', 'machine learning', 'deep learning',
                'neural network', 'artificial intelligence',
                'data mining', 'data warehouse'])
              or re.search(r'\bai\b|\bml\b', name_clean)):
            return 'AI & Data Science'
        elif any(k in name_clean for k in ['marketing', 'seo', 'social media']):
            return 'Digital Marketing'
        elif any(k in name for k in ['dbms', 'sql', 'join', 'normalization', 'cardinality', 'transaction',
                                  'concurrency', 'keys', 'stored procedure', 'algebra', 'schema',
                                  'mysql', 'relational', 'bookdealer', 'aggregate', 'database', 'insurance1', 'studentcourse']):
            return 'Database Management (DBMS)'
        elif any(k in name for k in ['ds', 'tree', 'queue', 'dequeue', 'stack', 'linked list',
                                    'dijkstra', 'mergesort', 'maxmin', 'tsp', 'algorithm', 'recursion', 'binary_tree', 'circular queue', 'priority queue', 'infix to postfix', 'traversal', 'recursiondms', 'recurssiondms', 'mergesor', 'djiktras']):
            return 'Data Structures & Algorithms'
        elif 'python' in name:
            return 'Python Programming'
        elif any(k in name for k in ['c program', 'c_language', 'tokens in c', 'constants', 'data types',
                                    'bpops', 'loop', 'conditional', 'switch case', 'arrays in c',
                                    'functions in c', 'strings in c', 'operators in c', 'introduction to c',
                                    'structure of c', 'comments in c', 'c tokens', 'symbolic constants',
                                    'casting in c', 'type conversion', 'natural_nos', 'multiplication_table', 'matrix programs']):
            return 'C Programming'
        elif any(k in name for k in ['unix', 'linux', 'vi editor', 'shell', 'vieditor']):
            return 'Operating Systems & Linux'
        elif any(k in name for k in ['html', 'css', 'javascript', 'canvas', 'js_']):
            return 'Web Technology'
        elif any(k in name for k in ['cma', 'block diagram of computer', 'computer & block diagram']):
            return 'Computer Architecture (CMA)'
        elif any(k in name for k in ['matrix', 'proofs', 'sequence']):
            return 'Mathematics & Discrete Structures'
        else:
            return 'General / Other Materials'

    if os.path.exists(resources_dir):
        for f in os.listdir(resources_dir):
            f_lower = f.lower()
            if f_lower.endswith(('.pdf', '.pptx', '.ppt', '.docx', '.doc', '.txt')):
                if f_lower.endswith('.pdf'):
                    icon = 'fa-file-pdf'
                    color = 'text-red-500'
                    bg_color = 'bg-red-50'
                    file_type = 'PDF Document'
                    file_type_class = 'pdf'
                elif f_lower.endswith(('.pptx', '.ppt')):
                    icon = 'fa-file-powerpoint'
                    color = 'text-orange-500'
                    bg_color = 'bg-orange-50'
                    file_type = 'Presentation'
                    file_type_class = 'presentation'
                elif f_lower.endswith('.txt'):
                    icon = 'fa-file-alt'
                    color = 'text-slate-500'
                    bg_color = 'bg-slate-50'
                    file_type = 'Text Notes'
                    file_type_class = 'word'
                else: # .docx, .doc
                    icon = 'fa-file-word'
                    color = 'text-blue-500'
                    bg_color = 'bg-blue-50'
                    file_type = 'Word Document'
                    file_type_class = 'word'
                
                subject_name = classify_file(f)
                file_obj = {
                    'name': f,
                    'icon': icon,
                    'color': color,
                    'bg_color': bg_color,
                    'file_type': file_type,
                    'file_type_class': file_type_class,
                    'subject': subject_name
                }
                
                template_resources.append(file_obj)
                subjects_map[subject_name].append(file_obj)
                
    # Format sorted subjects list for template rendering
    subjects_list = []
    preferred_order = [
        'C Programming',
        'Python Programming',
        'PHP Programming',
        'Data Structures & Algorithms',
        'Database Management (DBMS)',
        'AI & Data Science',
        'Operating Systems & Linux',
        'Web Technology',
        'Digital Marketing',
        'Computer Architecture (CMA)',
        'Mathematics & Discrete Structures',
        'General / Other Materials'
    ]
    
    for subject in preferred_order:
        files = subjects_map[subject]
        if files:
            subjects_list.append({
                'name': subject,
                'files': sorted(files, key=lambda x: x['name']),
                'count': len(files),
                'safe_id': subject.replace(' ', '_').replace('&', 'and').replace('(', '').replace(')', '')
            })
            
    # ── Dedicated tab file lists ──────────────────────────────────────────
    php_files = sorted(subjects_map['PHP Programming'],       key=lambda x: x['name'])
    ai_files  = sorted(subjects_map['AI & Data Science'],     key=lambda x: x['name'])
    dm_files  = sorted(subjects_map['Digital Marketing'],     key=lambda x: x['name'])

    return render(request, "student/resources_landing.html", {
        "is_locked": False,
        "template_resources": template_resources,
        "subjects": subjects_list,
        "php_files": php_files,
        "ai_files":  ai_files,
        "dm_files":  dm_files,
    })

def practice(request):
    if not request.user.is_authenticated:
        messages.info(request, "Login Required: Professional mock tests are only available to registered students. Please login first.")
        return redirect('/login/?next=/practice/')
    return render(request, "student/practice.html")

def about(request):
    return render(request, "about.html")

def placements(request):
    return render(request, "placements.html")

def contact(request):
    return render(request, "contact.html")

def video_tutorial(request):
    if not request.user.is_authenticated:
        messages.info(request, "Login Required: Video tutorials are only available to registered students. Please login first.")
        return redirect('/login/?next=/video-tutorial/')
    return render(request, "student/video_resource.html")

# AJAX LOGIN (for modal popup on landing page)
def ajax_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # SMTP Email: Send Successful Login Alert
            if user.email:
                try:
                    send_mail(
                        subject='Login Alert - JSS Campus Placement Portal',
                        message=f'Hello {user.username},\n\nYou have successfully logged in to your account on the JSS Campus Placement Portal. Thank you and welcome!\n\nIf this was not you, please contact support immediately.',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=True,
                    )
                except Exception as e:
                    pass
            
            # Determine appropriate redirect URL
            if user.is_superuser or user.is_staff or hasattr(user, 'placementofficer'):
                redirect_url = '/placement_app/admin_dashboard/'
            elif Company.objects.filter(user=user).exists():
                redirect_url = '/company/home/'
            else:
                # If they tried to access a specific resource, let the frontend use that, otherwise default to home
                redirect_url = '/student/home/'
                
            return JsonResponse({'success': True, 'message': 'Login successful!', 'redirect_url': redirect_url})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid username or password.'}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request.'}, status=405)

# AJAX REGISTER (for in-modal signup on landing page)
def ajax_register(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # Validation
        if not re.match(r'^[A-Za-z]+$', username):
            return JsonResponse({'success': False, 'message': 'Username should contain only letters.'}, status=400)

        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$'
        if not re.match(password_pattern, password):
            return JsonResponse({'success': False, 'message': 'Password must contain uppercase, lowercase, number, special character and minimum 8 characters.'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'message': 'Username already exists.'}, status=400)

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            
            # SMTP Email: Send Welcome Email
            try:
                subject = "Welcome to My Website"
                html_message = render_to_string("emails/welcome_email.html", {
                    "name": username,
                    "email": email
                })
                plain_message = strip_tags(html_message)

                send_mail(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    html_message=html_message,
                    fail_silently=False
                )
            except Exception as e:
                print("Email error:", e)

            return JsonResponse({'success': True, 'message': 'Registration successful! Please login.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error during registration: {str(e)}'}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request.'}, status=405)


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser or user.is_staff or hasattr(user, 'placementofficer'):
                login(request, user)
                return redirect('placementhome')   # → /placement_app/admin_dashboard/
            else:
                messages.error(request, "Access Denied: This account does not have admin privileges.")
        else:
            messages.error(request, "Invalid username or password. Please try again.")
        return redirect('admin_login')
    return render(request, 'admin_login.html')


# views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from placement_app.models import JobRequirement, JobApplication, Student

@login_required(login_url='login')
def job_detail(request, job_id):
    # Get the job
    job = get_object_or_404(JobRequirement, id=job_id)
    
    # Get the student
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Please complete your student profile first.")
        return redirect('home')
    
    # Check if already applied
    has_applied = JobApplication.objects.filter(student=student, job=job).exists()
    
    # Check eligibility
    is_eligible = True
    eligibility_messages = []
    
    if student.cgpa < job.min_cgpa:
        is_eligible = False
        eligibility_messages.append(f"CGPA requirement: {job.min_cgpa} (Your CGPA: {student.cgpa})")
    
    if student.backlogs > job.max_backlogs:
        is_eligible = False
        eligibility_messages.append(f"Maximum backlogs allowed: {job.max_backlogs} (Your backlogs: {student.backlogs})")
    
    if job.eligible_departments:
        eligible_depts = [d.strip().lower() for d in job.eligible_departments.split(',')]
        if student.department.lower() not in eligible_depts:
            is_eligible = False
            eligibility_messages.append(f"Your department ({student.department}) is not eligible")
    
    # Get similar jobs (same company or same type)
    similar_jobs = JobRequirement.objects.filter(
        company=job.company
    ).exclude(id=job.id)[:3]
    
    context = {
        'job': job,
        'student': student,
        'has_applied': has_applied,
        'is_eligible': is_eligible,
        'eligibility_messages': eligibility_messages,
        'similar_jobs': similar_jobs,
    }
    
    return render(request, 'student/job_detail.html', context)

# views.py
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from io import BytesIO
from datetime import datetime

@login_required
def generate_resume(request):
    """Generate a professional PDF resume"""
    
    # Get form data from request
    role = request.GET.get('role', 'Software Developer')
    summary = request.GET.get('summary', '')
    skills = request.GET.get('skills', '')
    backlogs = request.GET.get('backlogs', '0')
    experience = request.GET.get('experience', '')
    education = request.GET.get('education', '')
    project = request.GET.get('project', '')
    awards = request.GET.get('awards', '')
    
    # Get student data
    try:
        student = Student.objects.get(user=request.user)
        name = request.user.get_full_name() or request.user.username
        email = request.user.email
        phone = student.user.email  # You might want to add phone to student model
        cgpa = student.cgpa
        department = student.department
        course = student.course
        college = student.college.name if student.college else "JSS College"
    except:
        name = request.user.get_full_name() or request.user.username
        email = request.user.email
        phone = "Not Provided"
        cgpa = "N/A"
        department = "Computer Science"
        course = "B.E/B.Tech"
        college = "JSS Science and Technology University"
    
    # Create PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{name.replace(" ", "_")}_Resume.pdf"'
    
    # Create PDF document
    doc = SimpleDocTemplate(response, pagesize=A4, 
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=72)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=6,
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#4b5563'),
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#3b82f6'),
        spaceBefore=12,
        spaceAfter=6,
        borderPadding=5
    )
    
    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        alignment=TA_LEFT
    )
    
    # Header Section
    elements.append(Paragraph(name, title_style))
    
    # Contact info
    contact_info = f"{email} | {phone} | {college}"
    elements.append(Paragraph(contact_info, subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#3b82f6'), spaceBefore=5, spaceAfter=10))
    
    # Professional Summary
    if summary:
        elements.append(Paragraph("Professional Summary", section_style))
        elements.append(Paragraph(summary, normal_style))
        elements.append(Spacer(1, 10))
    
    # Education Section
    elements.append(Paragraph("Education", section_style))
    education_data = [
        ['Degree', 'Institution', 'CGPA/Percentage'],
        [course, college, str(cgpa)],
    ]
    if education:
        edu_text = Paragraph(education, normal_style)
        elements.append(edu_text)
    else:
        edu_table = Table(education_data, colWidths=[2*inch, 3*inch, 1.5*inch])
        edu_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ]))
        elements.append(edu_table)
    elements.append(Spacer(1, 10))
    
    # Technical Skills
    if skills:
        elements.append(Paragraph("Technical Skills", section_style))
        skills_list = skills.split(',')
        skills_html = "<ul>"
        for skill in skills_list[:10]:  # Limit to 10 skills
            skills_html += f"<li>{skill.strip()}</li>"
        skills_html += "</ul>"
        elements.append(Paragraph(skills_html, normal_style))
        elements.append(Spacer(1, 10))
    
    # Projects
    if project:
        elements.append(Paragraph("Academic Projects", section_style))
        elements.append(Paragraph(project, normal_style))
        elements.append(Spacer(1, 10))
    
    # Experience / Internships
    if experience:
        elements.append(Paragraph("Experience / Internships", section_style))
        elements.append(Paragraph(experience, normal_style))
        elements.append(Spacer(1, 10))
    
    # Certifications & Achievements
    if awards:
        elements.append(Paragraph("Certifications & Achievements", section_style))
        awards_list = awards.split(',')
        awards_html = "<ul>"
        for award in awards_list[:5]:
            awards_html += f"<li>{award.strip()}</li>"
        awards_html += "</ul>"
        elements.append(Paragraph(awards_html, normal_style))
        elements.append(Spacer(1, 10))
    
    # Backlogs (only show if > 0)
    if backlogs and int(backlogs) > 0:
        elements.append(Paragraph("Additional Information", section_style))
        elements.append(Paragraph(f"Active Backlogs: {backlogs}", normal_style))
        elements.append(Spacer(1, 10))
    
    # Footer
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceBefore=20))
    footer_text = f"Generated on {datetime.now().strftime('%B %d, %Y')}"
    elements.append(Paragraph(footer_text, subtitle_style))
    
    # Build PDF
    doc.build(elements)
    
    return response


@login_required(login_url='login')
def submit_practice_attempt(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Only POST requests allowed'}, status=405)
    
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Student profile not found'}, status=404)
        
    try:
        import json
        data = json.loads(request.body)
        category = data.get('category')
        score = int(data.get('score', 0))
        total_questions = int(data.get('total_questions', 10))
        
        if not category:
            return JsonResponse({'success': False, 'message': 'Category is required'}, status=400)
            
        # Create attempt
        attempt = PracticeAttempt.objects.create(
            student=student,
            category=category,
            score=score,
            total_questions=total_questions
        )
        
        # Create notification
        category_names = {
            'quant': 'Quantitative Aptitude',
            'logic': 'Logical Reasoning',
            'dsa': 'Data Structures & Algorithms',
            'cs_core': 'Computer Science Core',
            'hr': 'Scenario Based (HR)'
        }
        cat_display = category_names.get(category, category.title())
        percentage = int((score / total_questions) * 100)
        
        Notification.objects.create(
            student=student,
            message=f"Completed {cat_display} Practice Test: scored {score}/{total_questions} ({percentage}%). Keep it up!",
            is_read=False
        )
        
        return JsonResponse({
            'success': True, 
            'message': 'Practice score submitted successfully!',
            'score': score,
            'total_questions': total_questions
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)


@login_required(login_url='login')
def get_progress_stats(request):
    try:
        student = Student.objects.get(user=request.user)
        my_apps = JobApplication.objects.filter(student=student)
        total_applied = my_apps.count()
        total_shortlisted = my_apps.filter(status='Shortlisted').count()
        total_selected = my_apps.filter(status='Selected').count()
    except Student.DoesNotExist:
        return JsonResponse({
            'profile_completeness': 0,
            'practice_score': 0,
            'interview_readiness': 0,
            'total_applied': 0,
            'total_shortlisted': 0,
            'total_selected': 0
        })
        
    # Calculate stats
    # Profile completeness
    profile_fields = [
        student.registration_number, 
        student.department, 
        student.course, 
        student.year, 
        student.cgpa, 
        student.percentage_10th, 
        student.percentage_12th, 
        student.resume
    ]
    filled_fields = sum(1 for f in profile_fields if f)
    profile_completeness = int((filled_fields / len(profile_fields)) * 100)
    
    # Practice score
    attempts = PracticeAttempt.objects.filter(student=student)
    if attempts.exists():
        total_score = sum(a.score for a in attempts)
        total_possible = sum(a.total_questions for a in attempts)
        practice_score = int((total_score / total_possible) * 100)
    else:
        practice_score = int((student.cgpa / 10 * 70)) if student.cgpa else 60
        
    if practice_score > 100: practice_score = 100
    if practice_score < 30: practice_score = 30
    
    # Interview readiness
    results = InterviewResult.objects.filter(application__student=student)
    cleared_rounds = results.filter(result='Cleared').count()
    
    unique_categories = attempts.values_list('category', flat=True).distinct().count()
    practice_bonus = min(30, unique_categories * 6)
    app_bonus = min(15, total_applied * 5)
    interview_bonus = min(15, cleared_rounds * 10)
    
    interview_readiness = 40 + practice_bonus + app_bonus + interview_bonus
    if interview_readiness > 100: interview_readiness = 100
    
    return JsonResponse({
        'profile_completeness': profile_completeness,
        'practice_score': practice_score,
        'interview_readiness': interview_readiness,
        'total_applied': total_applied,
        'total_shortlisted': total_shortlisted,
        'total_selected': total_selected
    })