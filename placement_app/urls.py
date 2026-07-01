from django.urls import path
from . import views

urlpatterns = [
    # ── ADD FORMS ──────────────────────────────────
    path('college/', views.College_form, name='college'),
    path('placementofficer/', views.placementofficer_form, name='placementofficer'),
    path('student/', views.Student_form, name='student'),
    path('company/', views.company_form, name='company'),
    path('jobrequirement/', views.JobRequirement_form, name='jobrequirement'),
    path('jobapplication/', views.JobApplication_form, name='jobapplication'),
    path('interviewround/', views.InterviewRound_form, name='interviewround'),
    path('interviewresult/', views.InterviewResult_form, name='interviewresult'),
    path('notification/', views.Notification_form, name='notification'),

    # ── DASHBOARD ──────────────────────────────────
    path('admin_dashboard/', views.admin_dashboard, name='placementhome'),

    # ── LIST VIEWS ─────────────────────────────────
    path('colleged/', views.college_view, name='college_view'),
    path('officerd/', views.officer_view, name='placementofficer_view'),
    path('studentd/', views.student_view, name='student_view'),
    path('companyd/', views.company_view, name='company_view'),
    path('jobd/', views.job_view, name='jobrequirement_view'),
    path('applicationd/', views.jobapplication_view, name='jobapplication_view'),
    path('roundd/', views.interviewround_view, name='interviewround_view'),
    path('resultd/', views.interviewresult_view, name='interviewresult_view'),
    path('notifyd/', views.notification_view, name='notification_view'),

    # ── EDIT ───────────────────────────────────────
    path('college/edit/<int:pk>/', views.college_edit, name='college_edit'),
    path('officer/edit/<int:pk>/', views.officer_edit, name='officer_edit'),
    path('student/edit/<int:pk>/', views.student_edit, name='student_edit'),
    path('company/edit/<int:pk>/', views.company_edit, name='company_edit'),
    path('jobrequirement/edit/<int:pk>/', views.jobrequirement_edit, name='jobrequirement_edit'),
    path('jobapplication/edit/<int:pk>/', views.jobapplication_edit, name='jobapplication_edit'),
    path('interviewround/edit/<int:pk>/', views.interviewround_edit, name='interviewround_edit'),
    path('interviewresult/edit/<int:pk>/', views.interviewresult_edit, name='interviewresult_edit'),
    path('notification/edit/<int:pk>/', views.notification_edit, name='notification_edit'),

    # ── DELETE ─────────────────────────────────────
    path('college/delete/<int:pk>/', views.college_delete, name='college_delete'),
    path('officer/delete/<int:pk>/', views.officer_delete, name='officer_delete'),
    path('student/delete/<int:pk>/', views.student_delete, name='student_delete'),
    path('company/delete/<int:pk>/', views.company_delete, name='company_delete'),
    path('jobrequirement/delete/<int:pk>/', views.jobrequirement_delete, name='jobrequirement_delete'),
    path('jobapplication/delete/<int:pk>/', views.jobapplication_delete, name='jobapplication_delete'),
    path('interviewround/delete/<int:pk>/', views.interviewround_delete, name='interviewround_delete'),
    path('interviewresult/delete/<int:pk>/', views.interviewresult_delete, name='interviewresult_delete'),
    path('notification/delete/<int:pk>/', views.notification_delete, name='notification_delete'),
]

