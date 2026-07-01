from django.contrib import admin
from .models import (
    College, PlacementOfficer, Student, Company,
    JobRequirement, JobApplication, InterviewRound,
    InterviewResult, Notification
)

# ──────────────────────────────────────────────
# Admin site branding
# ──────────────────────────────────────────────
admin.site.site_header  = "Campus Placement Admin"
admin.site.site_title   = "Campus Placement Portal"
admin.site.index_title  = "Welcome to the Admin Dashboard"


# ──────────────────────────────────────────────
# 1. COLLEGE
# ──────────────────────────────────────────────
@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'code', 'email', 'phone', 'created_at')
    search_fields = ('name', 'code', 'email')
    list_filter   = ('created_at',)
    ordering      = ('-created_at',)
    fieldsets = (
        ('Basic Info',   {'fields': ('name', 'code', 'address')}),
        ('Contact',      {'fields': ('email', 'phone')}),
    )


# ──────────────────────────────────────────────
# 2. PLACEMENT OFFICER
# ──────────────────────────────────────────────
@admin.register(PlacementOfficer)
class PlacementOfficerAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'college', 'designation', 'phone')
    search_fields = ('user__username', 'user__email', 'college__name', 'designation')
    list_filter   = ('college', 'designation')
    ordering      = ('user__username',)
    fieldsets = (
        ('Account',   {'fields': ('user',)}),
        ('Details',   {'fields': ('college', 'designation', 'phone')}),
    )


# ──────────────────────────────────────────────
# 3. STUDENT
# ──────────────────────────────────────────────
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'college', 'registration_number',
                     'department', 'course', 'year', 'cgpa', 'backlogs')
    search_fields = ('user__username', 'registration_number', 'department', 'course')
    list_filter   = ('college', 'department', 'course', 'year')
    ordering      = ('user__username',)
    fieldsets = (
        ('Account',       {'fields': ('user', 'college', 'registration_number')}),
        ('Academic',      {'fields': ('department', 'course', 'year', 'cgpa',
                                      'percentage_10th', 'percentage_12th', 'backlogs')}),
        ('Resume',        {'fields': ('resume',)}),
    )


# ──────────────────────────────────────────────
# 4. COMPANY
# ──────────────────────────────────────────────
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'user', 'hr_name', 'hr_email', 'hr_phone', 'created_by', 'created_at')
    search_fields = ('name', 'hr_name', 'hr_email', 'user__username')
    list_filter   = ('created_at', 'created_by')
    ordering      = ('-created_at',)
    fieldsets = (
        ('Company Info',  {'fields': ('user', 'name', 'website', 'description')}),
        ('HR Details',    {'fields': ('hr_name', 'hr_email', 'hr_phone')}),
        ('Meta',          {'fields': ('created_by',)}),
    )


# ──────────────────────────────────────────────
# 5. JOB REQUIREMENT
# ──────────────────────────────────────────────
@admin.register(JobRequirement)
class JobRequirementAdmin(admin.ModelAdmin):
    list_display  = ('id', 'title', 'company', 'job_type', 'location',
                     'package', 'min_cgpa', 'max_backlogs', 'deadline')
    search_fields = ('title', 'company__name', 'location', 'eligible_departments')
    list_filter   = ('job_type', 'company', 'deadline')
    ordering      = ('-deadline',)
    fieldsets = (
        ('Job Info',      {'fields': ('company', 'title', 'description', 'location', 'package', 'job_type')}),
        ('Eligibility',   {'fields': ('min_cgpa', 'max_backlogs', 'eligible_departments', 'deadline')}),
    )


# ──────────────────────────────────────────────
# 6. JOB APPLICATION
# ──────────────────────────────────────────────
@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display  = ('id', 'student', 'job', 'status', 'applied_at')
    search_fields = ('student__user__username', 'job__title', 'job__company__name')
    list_filter   = ('status', 'applied_at', 'job__company')
    ordering      = ('-applied_at',)
    fieldsets = (
        ('Application',  {'fields': ('student', 'job', 'status')}),
    )


# ──────────────────────────────────────────────
# 7. INTERVIEW ROUND
# ──────────────────────────────────────────────
@admin.register(InterviewRound)
class InterviewRoundAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'job', 'round_type', 'scheduled_date')
    search_fields = ('name', 'job__title', 'job__company__name')
    list_filter   = ('round_type', 'scheduled_date')
    ordering      = ('scheduled_date',)
    fieldsets = (
        ('Round Info',  {'fields': ('job', 'name', 'round_type', 'scheduled_date')}),
    )


# ──────────────────────────────────────────────
# 8. INTERVIEW RESULT
# ──────────────────────────────────────────────
@admin.register(InterviewResult)
class InterviewResultAdmin(admin.ModelAdmin):
    list_display  = ('id', 'application', 'round', 'result', 'short_remarks')
    search_fields = ('application__student__user__username', 'round__name', 'result')
    list_filter   = ('result', 'round__round_type')
    ordering      = ('application',)
    fieldsets = (
        ('Result',  {'fields': ('application', 'round', 'result', 'remarks')}),
    )

    @admin.display(description='Remarks')
    def short_remarks(self, obj):
        return obj.remarks[:60] + '…' if len(obj.remarks) > 60 else obj.remarks


# ──────────────────────────────────────────────
# 9. NOTIFICATION
# ──────────────────────────────────────────────
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display  = ('id', 'student', 'is_read', 'short_message', 'created_at')
    search_fields = ('student__user__username', 'message')
    list_filter   = ('is_read', 'created_at')
    ordering      = ('-created_at',)
    fieldsets = (
        ('Notification',  {'fields': ('student', 'message', 'is_read')}),
    )

    @admin.display(description='Message')
    def short_message(self, obj):
        return obj.message[:80] + '…' if len(obj.message) > 80 else obj.message

