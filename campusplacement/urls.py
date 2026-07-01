"""
URL configuration for campusplacement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from campusplacement import views
from django.urls import include, path

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),

    # Login Page
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('refresh-captcha/', views.refresh_captcha, name='refresh_captcha'),

    # Forgot Password Page
    path('forgot-password/', views.forgot_password, name='forgot_password'),

    # Registration Page
    path('register/', views.register, name='register'),

    # Home / Dashboard Page
    path('student/home/', views.home, name='home'),
    path('student/home/', views.home, name='student_home'),
    path('student/resume/download/', views.generate_resume, name='generate_resume'),
    path('company/home/', views.company_home, name='company_home'),
    path('company/post-job/', views.company_post_job, name='company_post_job'),
    path('company/applications/', views.company_applications, name='company_applications'),
    path('company/interviews/', views.company_interviews, name='company_interviews'),
    path('company/profile/', views.company_profile, name='company_profile'),
    
    
    path('companies/', views.companies, name='companies'),
    path('student/job/<int:job_id>/', views.job_detail, name='job_detail'),  # Add this line
    path('apply-job-ajax/', views.apply_job_ajax, name='apply_job_ajax'),
    path('generate-resume/', views.generate_resume, name='generate_resume'),
    path('apply_job/', views.apply_job, name='apply_job'),
    path('applications/', views.applications, name='applications'),
    path('resources/', views.resources, name='resources'),
    path('practice/', views.practice, name='practice'),
    path('video-tutorial/', views.video_tutorial, name='video_resource'),
    path('about/', views.about, name='about'),
    path('placements/', views.placements, name='placements-info'),
    path('contact/', views.contact, name='contact'),
    path('ajax-login/', views.ajax_login, name='ajax_login'),
    path('ajax-register/', views.ajax_register, name='ajax_register'),
    path('placement_app/', include('placement_app.urls')),
    path('admin-login/', views.admin_login, name='admin_login'),

    # Company Login (role-restricted – only Company users allowed)
    path('company-login/', views.company_login, name='company_login'),

    # Student progress and practice submit endpoints
    path('student/practice/submit/', views.submit_practice_attempt, name='submit_practice_attempt'),
    path('student/api/progress-stats/', views.get_progress_stats, name='get_progress_stats'),
]



