from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ==========================================
# 1. COLLEGE MODEL
# ==========================================
class College(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    email = models.EmailField()
    phone = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ==========================================
# 2. PLACEMENT OFFICER
# ==========================================
class PlacementOfficer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    phone = models.IntegerField()
    designation = models.CharField(max_length=100, default="Placement Officer")

    def __str__(self):
        return f"{self.user.username} - {self.college.name}"


# ==========================================
# 3. STUDENT
# ==========================================
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    registration_number = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=20)
    course = models.CharField(max_length=20)
    year = models.IntegerField()

    cgpa = models.FloatField()
    percentage_10th = models.FloatField()
    percentage_12th = models.FloatField()

    backlogs = models.IntegerField(default=0)
    resume = models.FileField(upload_to="resumes/", null=True, blank=True)

    def __str__(self):
        return self.user.username


# ==========================================
# 4. COMPANY
# ==========================================
class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    website = models.URLField(blank=True)
    description = models.TextField()
    hr_name = models.CharField(max_length=100)
    hr_email = models.EmailField()
    hr_phone = models.CharField(max_length=10)
    created_by = models.ForeignKey(
        PlacementOfficer,
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ==========================================
# 5. JOB REQUIREMENT
# ==========================================
class JobRequirement(models.Model):
    JOB_TYPE_CHOICES = (
        ("Full Time", "Full Time"),
        ("Internship", "Internship"),
        ("Contract", "Contract"),
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    description = models.TextField()
    location = models.CharField(max_length=100)
    package = models.CharField(max_length=50)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)

    min_cgpa = models.FloatField(default=0.0)
    max_backlogs = models.IntegerField(default=0)
    eligible_departments = models.CharField(max_length=255)

    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.company.name}"


# ==========================================
# 6. JOB APPLICATION
# ==========================================
class JobApplication(models.Model):
    STATUS_CHOICES = (
        ("Applied", "Applied"),
        ("Shortlisted", "Shortlisted"),
        ("Rejected", "Rejected"),
        ("Selected", "Selected"),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job = models.ForeignKey(JobRequirement, on_delete=models.CASCADE)

    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Applied"
    )

    def __str__(self):
        return f"{self.student.user.username} - {self.job.title}"


# ==========================================
# 7. INTERVIEW ROUNDS
# ==========================================
class InterviewRound(models.Model):
    ROUND_TYPE = (
        ("Aptitude", "Aptitude"),
        ("Technical", "Technical"),
        ("HR", "HR"),
        ("Group Discussion", "Group Discussion"),
    )

    job = models.ForeignKey(JobRequirement, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    round_type = models.CharField(max_length=50, choices=ROUND_TYPE)
    scheduled_date = models.DateTimeField()

    def __str__(self):
        return f"{self.job.title} - {self.name}"


# ==========================================
# 8. INTERVIEW RESULT
# ==========================================
class InterviewResult(models.Model):
    RESULT_STATUS = (
        ("Cleared", "Cleared"),
        ("Not Cleared", "Not Cleared"),
    )

    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE)
    round = models.ForeignKey(InterviewRound, on_delete=models.CASCADE)
    result = models.CharField(max_length=20, choices=RESULT_STATUS)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.application.student.user.username} - {self.round.name}"


# ==========================================
# 9. NOTIFICATION SYSTEM
# ==========================================
class Notification(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Notification for {self.student.user.username}"