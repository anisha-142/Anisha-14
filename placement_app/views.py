from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User

# DASHBOARD
def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not (request.user.is_superuser or request.user.is_staff or hasattr(request.user, 'placementofficer')):
        return redirect('home')
        
    from django.db.models import Count
    import json
    
    # Base Metrics
    total_colleges = College.objects.count()
    total_officers = PlacementOfficer.objects.count()
    total_students = Student.objects.count()
    total_companies = Company.objects.count()
    total_jobs = JobRequirement.objects.count()
    total_applications = JobApplication.objects.count()
    total_rounds = InterviewRound.objects.count()
    total_results = InterviewResult.objects.count()
    total_notifications = Notification.objects.count()
    
    # Application statuses distribution
    status_data = JobApplication.objects.values('status').annotate(count=Count('status'))
    status_counts = {item['status']: item['count'] for item in status_data}
    chart_status_data = {
        'Applied': status_counts.get('Applied', 0),
        'Shortlisted': status_counts.get('Shortlisted', 0),
        'Selected': status_counts.get('Selected', 0),
        'Rejected': status_counts.get('Rejected', 0),
    }
    
    # Job types distribution
    type_data = JobRequirement.objects.values('job_type').annotate(count=Count('job_type'))
    type_counts = {item['job_type']: item['count'] for item in type_data}
    chart_type_data = {
        'Full-time': type_counts.get('Full-time', 0) + type_counts.get('Full Time', 0),
        'Internship': type_counts.get('Internship', 0),
        'Contract': type_counts.get('Contract', 0),
        'Part-time': type_counts.get('Part-time', 0) + type_counts.get('Part Time', 0),
    }
    
    context = {
        'total_colleges': total_colleges,
        'total_officers': total_officers,
        'total_students': total_students,
        'total_companies': total_companies,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'total_rounds': total_rounds,
        'total_results': total_results,
        'total_notifications': total_notifications,
        'status_json': json.dumps(chart_status_data),
        'type_json': json.dumps(chart_type_data),
    }
    
    return render(request, 'admin/dashboard.html', context)

# 1. COLLEGE FORM
def College_form(request):
    if request.method == "POST":
        try:
            Name = request.POST.get('name')
            Code = request.POST.get('code')
            Address = request.POST.get('address')
            Email = request.POST.get('email')
            Phone = request.POST.get('phone')
            
            College.objects.create(
                name=Name,
                code=Code,
                address=Address,
                email=Email,
                phone=Phone
            )
            messages.success(request, f"College '{Name}' added successfully!")
        except Exception as e:
            messages.error(request, f"Error adding college: {str(e)}")
            
    return render(request, 'admin/College.html')

# 2. PLACEMENT OFFICER FORM
def placementofficer_form(request):
    if request.method == "POST":
        try:
            user_id = request.POST.get('user')
            college_id = request.POST.get('college')
            phone = request.POST.get('phone')
            designation = request.POST.get('designation')
            
            user = User.objects.get(id=user_id)
            college = College.objects.get(id=college_id)
            
            PlacementOfficer.objects.create(
                user=user,
                college=college,
                phone=phone,
                designation=designation
            )
            messages.success(request, f"Placement Officer '{user.username}' added successfully!")
        except Exception as e:
            messages.error(request, f"Error adding placement officer: {str(e)}")
            
    users = User.objects.exclude(placementofficer__isnull=False).exclude(is_superuser=True)
    colleges = College.objects.all()
    return render(request, 'admin/placementofficer.html', {'users': users, 'colleges': colleges})

# 3. STUDENT FORM
def Student_form(request):
    if request.method == "POST":
        try:
            user_id = request.POST.get('user')
            college_id = request.POST.get('college')
            reg_no = request.POST.get('registration_number')
            dept = request.POST.get('department')
            course = request.POST.get('course')
            year = request.POST.get('year')
            cgpa = request.POST.get('cgpa')
            p10 = request.POST.get('percentage_10th')
            p12 = request.POST.get('percentage_12th')
            backlogs = request.POST.get('backlogs')
            resume = request.FILES.get('resume')
            
            user = User.objects.get(id=user_id)
            college = College.objects.get(id=college_id)
            
            Student.objects.create(
                user=user,
                college=college,
                registration_number=reg_no,
                department=dept,
                course=course,
                year=int(year),
                cgpa=float(cgpa),
                percentage_10th=float(p10),
                percentage_12th=float(p12),
                backlogs=int(backlogs or 0),
                resume=resume
            )
            messages.success(request, f"Student '{user.username}' added successfully!")
        except Exception as e:
            messages.error(request, f"Error adding student: {str(e)}")
            
    users = User.objects.exclude(student__isnull=False).exclude(is_superuser=True)
    all_users = User.objects.all() # Fallback for display if needed
    colleges = College.objects.all()
    return render(request, 'admin/student.html', {'users': users, 'colleges': colleges})

# 4. COMPANY FORM
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import transaction

def company_form(request):
    if request.method == "POST":
        try:
            with transaction.atomic():  # Ensures data consistency
                # Get form data
                username = request.POST.get('username')
                password = request.POST.get('password')
                email = request.POST.get('email')
                name = request.POST.get('name')
                website = request.POST.get('website')
                description = request.POST.get('description')
                hr_name = request.POST.get('hr_name')
                hr_email = request.POST.get('hr_email')
                hr_phone = request.POST.get('hr_phone')
                officer_id = request.POST.get('created_by')
                
                # Validate required fields
                if not all([username, password, email, name, hr_name, hr_email, hr_phone]):
                    messages.error(request, "Please fill all required fields")
                    return render(request, 'admin/company.html', get_context_data(request))
                
                # Check if username already exists
                if User.objects.filter(username=username).exists():
                    messages.error(request, f"Username '{username}' already exists")
                    return render(request, 'admin/company.html', get_context_data(request))
                
                # Check if email already exists
                if User.objects.filter(email=email).exists():
                    messages.error(request, f"Email '{email}' already exists")
                    return render(request, 'admin/company.html', get_context_data(request))
                
                # Create User
                user = User.objects.create(
                    username=username,
                    email=email,
                    password=make_password(password),  # Hash the password
                    is_active=True
                )
                
                # Create UserProfile for role management
                UserProfile.objects.create(
                    user=user,
                    role="COMPANY"
                )
                
                # Get Placement Officer (optional field)
                officer = None
                if officer_id:
                    try:
                        officer = PlacementOfficer.objects.get(id=officer_id)
                    except PlacementOfficer.DoesNotExist:
                        messages.warning(request, "Selected placement officer not found")
                
                # Create Company profile
                company = Company.objects.create(
                    user=user,
                    name=name,
                    website=website or "",  # Handle blank website
                    description=description,
                    hr_name=hr_name,
                    hr_email=hr_email,
                    hr_phone=hr_phone,
                    created_by=officer
                )
                
                messages.success(
                    request, 
                    f"Company '{name}' created successfully! Username: {username}"
                )
                return redirect('company_view')  # Or wherever you want to redirect
                
        except Exception as e:
            messages.error(request, f"Error adding company: {str(e)}")
            return render(request, 'admin/company.html', get_context_data(request))
    
    return render(request, 'admin/company.html', get_context_data(request))

def get_context_data(request):
    """Helper function to get context data for the form"""
    from django.contrib.auth.models import User
    
    # Get existing companies (to exclude their users)
    existing_company_users = Company.objects.values_list('user_id', flat=True)
    
    # Get users who are not assigned to any company and not superusers
    users = User.objects.exclude(
        id__in=existing_company_users
    ).exclude(
        is_superuser=True
    ).exclude(
        userprofile__role='STUDENT'  # Exclude students if they have profiles
    )
    
    officers = PlacementOfficer.objects.select_related('user', 'college').all()
    
    return {
        'users': users,
        'officers': officers,
        'roles': UserProfile.ROLE_CHOICES,
    }

# 5. JOB REQUIREMENT FORM
def JobRequirement_form(request):
    if request.method == "POST":
        try:
            company_id = request.POST.get('company')
            title = request.POST.get('title')
            desc = request.POST.get('description')
            loc = request.POST.get('location')
            pack = request.POST.get('package')
            jtype = request.POST.get('job_type')
            min_cgpa = request.POST.get('min_cgpa')
            max_bl = request.POST.get('max_backlogs')
            dept = request.POST.get('eligible_departments')
            deadline = request.POST.get('deadline')
            
            company = Company.objects.get(id=company_id)
            
            JobRequirement.objects.create(
                company=company,
                title=title,
                description=desc,
                location=loc,
                package=pack,
                job_type=jtype,
                min_cgpa=float(min_cgpa or 0.0),
                max_backlogs=int(max_bl or 0),
                eligible_departments=dept,
                deadline=deadline
            )
            messages.success(request, f"Job '{title}' for '{company.name}' added successfully!")
        except Exception as e:
            messages.error(request, f"Error adding job requirement: {str(e)}")
            
    companies = Company.objects.all()
    return render(request, 'admin/JobRequirement.html', {'companies': companies})

# 6. JOB APPLICATION FORM
def JobApplication_form(request):
    if request.method == "POST":
        try:
            student_id = request.POST.get('student')
            job_id = request.POST.get('job')
            status = request.POST.get('status')
            
            student = Student.objects.get(id=student_id)
            job = JobRequirement.objects.get(id=job_id)
            
            JobApplication.objects.create(
                student=student,
                job=job,
                status=status
            )
            messages.success(request, "Application submitted successfully!")
        except Exception as e:
            messages.error(request, f"Error submitting application: {str(e)}")
            
    students = Student.objects.all()
    jobs = JobRequirement.objects.all()
    return render(request, 'admin/JobApplication.html', {'students': students, 'jobs': jobs})

# 7. INTERVIEW ROUND FORM
def InterviewRound_form(request):
    if request.method == "POST":
        try:
            job_id = request.POST.get('job')
            name = request.POST.get('name')
            rtype = request.POST.get('round_type')
            sdate = request.POST.get('scheduled_date')
            
            job = JobRequirement.objects.get(id=job_id)
            
            InterviewRound.objects.create(
                job=job,
                name=name,
                round_type=rtype,
                scheduled_date=sdate
            )
            messages.success(request, f"Round '{name}' scheduled for '{job.title}'!")
        except Exception as e:
            messages.error(request, f"Error scheduling interview round: {str(e)}")
            
    jobs = JobRequirement.objects.all()
    return render(request, 'admin/InterviewRound.html', {'jobs': jobs})

# 8. INTERVIEW RESULT FORM
def InterviewResult_form(request):
    if request.method == "POST":
        try:
            app_id = request.POST.get('application')
            round_id = request.POST.get('round')
            res = request.POST.get('result')
            rem = request.POST.get('remarks')
            
            app = JobApplication.objects.get(id=app_id)
            iround = InterviewRound.objects.get(id=round_id)
            
            InterviewResult.objects.create(
                application=app,
                round=iround,
                result=res,
                remarks=rem
            )
            messages.success(request, "Result recorded successfully!")
        except Exception as e:
            messages.error(request, f"Error recording result: {str(e)}")
            
    apps = JobApplication.objects.all()
    rounds = InterviewRound.objects.all()
    return render(request, 'admin/InterviewResult.html', {'applications': apps, 'rounds': rounds})

# 9. NOTIFICATION FORM
def Notification_form(request):
    if request.method == "POST":
        try:
            student_id = request.POST.get('student')
            msg = request.POST.get('message')
            
            student = Student.objects.get(id=student_id)
            
            Notification.objects.create(
                student=student,
                message=msg
            )
            messages.success(request, f"Notification sent to '{student.user.username}'!")
        except Exception as e:
            messages.error(request, f"Error sending notification: {str(e)}")
            
    students = Student.objects.all()
    return render(request, 'admin/Notification.html', {'students': students})
def college_view(request):
    collegedetails=College.objects.all()
    return render(request,'admin/college__view.html',{'colleged':collegedetails})

def officer_view(request):
    officers=PlacementOfficer.objects.all()
    return render(request,'admin/placementofficer__view.html',{'officerd':officers})

def student_view(request):
    students=Student.objects.all()
    return render(request,'admin/student__view.html',{'studentd':students})

def company_view(request):
    companies=Company.objects.all()
    return render(request,'admin/company__view.html',{'companyd':companies})

def job_view(request):
    jobs=JobRequirement.objects.all()
    return render(request,'admin/jobrequirement__view.html',{'jobd':jobs})

def jobapplication_view(request):
    apps=JobApplication.objects.all()
    return render(request,'admin/jobapplication__view.html',{'jobapplicationd':apps})

def interviewround_view(request):
    rounds=InterviewRound.objects.all()
    return render(request,'admin/interviewround__view.html',{'interviewroundd':rounds})

def interviewresult_view(request):
    results=InterviewResult.objects.all()
    return render(request,'admin/interviewresult__view.html',{'interviewresultd':results})

def notification_view(request):
    notifications=Notification.objects.all()
    return render(request,'admin/notification__view.html',{'notificationd':notifications})

# ──────────────────────────────────────────────
# EDIT VIEWS
# ──────────────────────────────────────────────

def college_edit(request, pk):
    college = College.objects.get(id=pk)
    if request.method == "POST":
        try:
            college.name    = request.POST.get('name')
            college.code    = request.POST.get('code')
            college.address = request.POST.get('address')
            college.email   = request.POST.get('email')
            college.phone   = request.POST.get('phone')
            college.save()
            messages.success(request, f"College '{college.name}' updated successfully!")
        except Exception as e:
            messages.error(request, f"Error updating college: {str(e)}")
    return render(request, 'admin/edit_college.html', {'college': college})

def officer_edit(request, pk):
    officer = PlacementOfficer.objects.get(id=pk)
    if request.method == "POST":
        try:
            officer.user        = User.objects.get(id=request.POST.get('user'))
            officer.college     = College.objects.get(id=request.POST.get('college'))
            officer.phone       = request.POST.get('phone')
            officer.designation = request.POST.get('designation')
            officer.save()
            messages.success(request, "Placement Officer updated successfully!")
        except Exception as e:
            messages.error(request, f"Error updating officer: {str(e)}")
    users    = User.objects.all()
    colleges = College.objects.all()
    return render(request, 'admin/edit_placementofficer.html', {'officer': officer, 'users': users, 'colleges': colleges})

def student_edit(request, pk):
    student = Student.objects.get(id=pk)
    if request.method == "POST":
        try:
            student.user                = User.objects.get(id=request.POST.get('user'))
            student.college             = College.objects.get(id=request.POST.get('college'))
            student.registration_number = request.POST.get('registration_number')
            student.department          = request.POST.get('department')
            student.course              = request.POST.get('course')
            student.year                = int(request.POST.get('year'))
            student.cgpa                = float(request.POST.get('cgpa'))
            student.percentage_10th     = float(request.POST.get('percentage_10th'))
            student.percentage_12th     = float(request.POST.get('percentage_12th'))
            student.backlogs            = int(request.POST.get('backlogs', 0))
            if request.FILES.get('resume'):
                student.resume = request.FILES.get('resume')
            student.save()
            messages.success(request, "Student updated successfully!")
        except Exception as e:
            messages.error(request, f"Error updating student: {str(e)}")
    users    = User.objects.all()
    colleges = College.objects.all()
    return render(request, 'admin/edit_student.html', {'student': student, 'users': users, 'colleges': colleges})

def company_edit(request, pk):
    company = Company.objects.get(id=pk)
    if request.method == "POST":
        try:
            company.user        = User.objects.get(id=request.POST.get('user'))
            company.name        = request.POST.get('name')
            company.website     = request.POST.get('website')
            company.description = request.POST.get('description')
            company.hr_name     = request.POST.get('hr_name')
            company.hr_email    = request.POST.get('hr_email')
            company.hr_phone    = request.POST.get('hr_phone')
            officer_id          = request.POST.get('created_by')
            company.created_by  = PlacementOfficer.objects.get(id=officer_id) if officer_id else None
            company.save()
            messages.success(request, f"Company '{company.name}' updated successfully!")
        except Exception as e:
            messages.error(request, f"Error updating company: {str(e)}")
    users    = User.objects.all()
    officers = PlacementOfficer.objects.all()
    return render(request, 'admin/edit_company.html', {'company': company, 'users': users, 'officers': officers})

def jobrequirement_edit(request, pk):
    job = JobRequirement.objects.get(id=pk)
    if request.method == "POST":
        try:
            job.company              = Company.objects.get(id=request.POST.get('company'))
            job.title                = request.POST.get('title')
            job.description          = request.POST.get('description')
            job.location             = request.POST.get('location')
            job.package              = request.POST.get('package')
            job.job_type             = request.POST.get('job_type')
            job.min_cgpa             = float(request.POST.get('min_cgpa', 0.0))
            job.max_backlogs         = int(request.POST.get('max_backlogs', 0))
            job.eligible_departments = request.POST.get('eligible_departments')
            job.deadline             = request.POST.get('deadline')
            job.save()
            messages.success(request, f"Job '{job.title}' updated successfully!")
        except Exception as e:
            messages.error(request, f"Error updating job: {str(e)}")
    companies = Company.objects.all()
    return render(request, 'admin/edit_jobrequirement.html', {'job': job, 'companies': companies})

def jobapplication_edit(request, pk):
    application = JobApplication.objects.get(id=pk)
    if request.method == "POST":
        try:
            application.student = Student.objects.get(id=request.POST.get('student'))
            application.job     = JobRequirement.objects.get(id=request.POST.get('job'))
            application.status  = request.POST.get('status')
            application.save()
            messages.success(request, "Application updated successfully!")
        except Exception as e:
            messages.error(request, f"Error updating application: {str(e)}")
    students = Student.objects.all()
    jobs     = JobRequirement.objects.all()
    return render(request, 'admin/edit_jobapplication.html', {'application': application, 'students': students, 'jobs': jobs})

def interviewround_edit(request, pk):
    round_obj = InterviewRound.objects.get(id=pk)
    if request.method == "POST":
        try:
            round_obj.job            = JobRequirement.objects.get(id=request.POST.get('job'))
            round_obj.name           = request.POST.get('name')
            round_obj.round_type     = request.POST.get('round_type')
            round_obj.scheduled_date = request.POST.get('scheduled_date')
            round_obj.save()
            messages.success(request, f"Round '{round_obj.name}' updated successfully!")
        except Exception as e:
            messages.error(request, f"Error updating round: {str(e)}")
    jobs = JobRequirement.objects.all()
    return render(request, 'admin/edit_interviewround.html', {'round': round_obj, 'jobs': jobs})

def interviewresult_edit(request, pk):
    result = InterviewResult.objects.get(id=pk)
    if request.method == "POST":
        try:
            result.application = JobApplication.objects.get(id=request.POST.get('application'))
            result.round       = InterviewRound.objects.get(id=request.POST.get('round'))
            result.result      = request.POST.get('result')
            result.remarks     = request.POST.get('remarks', '')
            result.save()
            messages.success(request, "Interview result updated successfully!")
        except Exception as e:
            messages.error(request, f"Error updating result: {str(e)}")
    applications = JobApplication.objects.all()
    rounds       = InterviewRound.objects.all()
    return render(request, 'admin/edit_interviewresult.html', {'result': result, 'applications': applications, 'rounds': rounds})

def notification_edit(request, pk):
    notification = Notification.objects.get(id=pk)
    if request.method == "POST":
        try:
            notification.student = Student.objects.get(id=request.POST.get('student'))
            notification.message = request.POST.get('message')
            notification.is_read = 'is_read' in request.POST
            notification.save()
            messages.success(request, "Notification updated successfully!")
        except Exception as e:
            messages.error(request, f"Error updating notification: {str(e)}")
    students = Student.objects.all()
    return render(request, 'admin/edit_notification.html', {'notification': notification, 'students': students})

# ──────────────────────────────────────────────
# DELETE VIEWS
# ──────────────────────────────────────────────

def college_delete(request, pk):
    try:
        College.objects.get(id=pk).delete()
        messages.success(request, "College deleted successfully!")
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
    return redirect('college_view')

def officer_delete(request, pk):
    try:
        officer = PlacementOfficer.objects.get(id=pk)
        user = officer.user
        user.delete()
        messages.success(request, "Officer and associated user account deleted successfully!")
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
    return redirect('placementofficer_view')

def student_delete(request, pk):
    try:
        student = Student.objects.get(id=pk)
        user = student.user
        user.delete()
        messages.success(request, "Student and associated user account deleted successfully!")
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
    return redirect('student_view')

def company_delete(request, pk):
    try:
        company = Company.objects.get(id=pk)
        user = company.user
        user.delete()
        messages.success(request, "Company and associated user account deleted successfully!")
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
    return redirect('company_view')

def jobrequirement_delete(request, pk):
    try:
        JobRequirement.objects.get(id=pk).delete()
        messages.success(request, "Job requirement deleted successfully!")
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
    return redirect('jobrequirement_view')

def jobapplication_delete(request, pk):
    try:
        JobApplication.objects.get(id=pk).delete()
        messages.success(request, "Application deleted successfully!")
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
    return redirect('jobapplication_view')

def interviewround_delete(request, pk):
    try:
        InterviewRound.objects.get(id=pk).delete()
        messages.success(request, "Interview round deleted successfully!")
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
    return redirect('interviewround_view')

def interviewresult_delete(request, pk):
    try:
        InterviewResult.objects.get(id=pk).delete()
        messages.success(request, "Interview result deleted successfully!")
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
    return redirect('interviewresult_view')

def notification_delete(request, pk):
    try:
        Notification.objects.get(id=pk).delete()
        messages.success(request, "Notification deleted successfully!")
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
    return redirect('notification_view')
