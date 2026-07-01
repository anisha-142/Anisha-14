"""
seed_data.py — Populate the JSS Campus Placement portal with realistic demo data.

Run from: d:\Campusplacement\campusplacement\
Command : ..\env\Scripts\python.exe seed_data.py
"""

import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusplacement.settings')
django.setup()

from django.contrib.auth.models import User
from placement_app.models import (
    College, Company, JobRequirement, PlacementOfficer,
    Student, Notification, UserProfile
)

today = date.today()

# ──────────────────────────────────────────────────────────────────────────────
# 1. COLLEGE
# ──────────────────────────────────────────────────────────────────────────────
college, _ = College.objects.get_or_create(
    code='JSSSMI',
    defaults={
        'name': 'JSS SMI UG & PG Studies',
        'address': 'JSS Campus, Mysuru Road, Dharwad, Karnataka - 580003',
        'email': 'placement@jss.edu.in',
        'phone': '0836-2447465',
    }
)
print(f"✓ College: {college.name}")

# ──────────────────────────────────────────────────────────────────────────────
# 2. PLACEMENT OFFICER (admin account)
# ──────────────────────────────────────────────────────────────────────────────
officer_user, created = User.objects.get_or_create(
    username='placement_officer',
    defaults={
        'email': 'officer@jss.edu.in',
        'first_name': 'Placement',
        'last_name': 'Officer',
        'is_staff': True,
    }
)
if created:
    officer_user.set_password('Officer@123')
    officer_user.save()

officer, _ = PlacementOfficer.objects.get_or_create(
    user=officer_user,
    defaults={
        'college': college,
        'phone': '9876543210',
        'designation': 'Chief Placement Officer',
    }
)
print(f"✓ Placement Officer: {officer_user.username}")

# ──────────────────────────────────────────────────────────────────────────────
# 3. COMPANIES — 6 realistic IT/Tech companies
# ──────────────────────────────────────────────────────────────────────────────
COMPANIES = [
    {
        'username': 'infosys_hr',
        'name': 'Infosys Limited',
        'website': 'https://www.infosys.com',
        'description': 'Infosys is a global leader in next-generation digital services and consulting. We enable clients in more than 56 countries to navigate their digital transformation.',
        'hr_name': 'Priya Sharma',
        'hr_email': 'priya.sharma@infosys.com',
        'hr_phone': '080-28520261',
    },
    {
        'username': 'tcs_hr',
        'name': 'Tata Consultancy Services',
        'website': 'https://www.tcs.com',
        'description': 'TCS is an IT services, consulting, and business solutions organization that has been partnering with many of the world\'s largest businesses in their transformation journeys.',
        'hr_name': 'Rajesh Kumar',
        'hr_email': 'rajesh.kumar@tcs.com',
        'hr_phone': '022-67789999',
    },
    {
        'username': 'wipro_hr',
        'name': 'Wipro Technologies',
        'website': 'https://www.wipro.com',
        'description': 'Wipro Limited is a leading global information technology, consulting and business process services company. We harness the power of cognitive computing, hyper-automation, robotics, cloud, analytics and emerging technologies.',
        'hr_name': 'Anita Rao',
        'hr_email': 'anita.rao@wipro.com',
        'hr_phone': '080-28440011',
    },
    {
        'username': 'cognizant_hr',
        'name': 'Cognizant Technology Solutions',
        'website': 'https://www.cognizant.com',
        'description': 'Cognizant is one of the world\'s leading professional services companies, transforming clients\' business, operating, and technology models for the digital era.',
        'hr_name': 'Sunita Mehta',
        'hr_email': 'sunita.mehta@cognizant.com',
        'hr_phone': '044-42099000',
    },
    {
        'username': 'accenture_hr',
        'name': 'Accenture India',
        'website': 'https://www.accenture.com/in-en',
        'description': 'Accenture is a global professional services company with leading capabilities in digital, cloud and security. Combining unmatched experience and specialized skills across more than 40 industries.',
        'hr_name': 'Vikram Nair',
        'hr_email': 'vikram.nair@accenture.com',
        'hr_phone': '080-41089000',
    },
    {
        'username': 'amazon_hr',
        'name': 'Amazon Development Centre',
        'website': 'https://www.amazon.jobs/en/locations/india',
        'description': 'Amazon is guided by four principles: customer obsession rather than competitor focus, passion for invention, commitment to operational excellence, and long-term thinking.',
        'hr_name': 'Deepa Krishnan',
        'hr_email': 'deepa.krishnan@amazon.com',
        'hr_phone': '040-67280000',
    },
]

created_companies = {}
for c in COMPANIES:
    u, ucreated = User.objects.get_or_create(
        username=c['username'],
        defaults={'email': c['hr_email'], 'first_name': c['hr_name'].split()[0], 'last_name': c['hr_name'].split()[-1]}
    )
    if ucreated:
        u.set_password('Company@123')
        u.save()
        UserProfile.objects.get_or_create(user=u, defaults={'role': 'COMPANY'})

    company, _ = Company.objects.get_or_create(
        user=u,
        defaults={
            'name': c['name'],
            'website': c['website'],
            'description': c['description'],
            'hr_name': c['hr_name'],
            'hr_email': c['hr_email'],
            'hr_phone': c['hr_phone'],
            'created_by': officer,
        }
    )
    created_companies[c['name']] = company
    print(f"✓ Company: {company.name}")

# ──────────────────────────────────────────────────────────────────────────────
# 4. JOB REQUIREMENTS — 2–3 jobs per company
# ──────────────────────────────────────────────────────────────────────────────
JOBS = [
    # Infosys
    {
        'company': 'Infosys Limited',
        'title': 'Systems Engineer',
        'description': 'Join Infosys as a Systems Engineer and work on cutting-edge enterprise software solutions. You will be part of a global team building scalable, cloud-native applications using Java, Spring Boot, and AWS. Responsibilities include requirement analysis, design, development, and testing of software modules.',
        'location': 'Bengaluru / Pune / Hyderabad',
        'package': '4.5',
        'job_type': 'Full Time',
        'min_cgpa': 6.0,
        'max_backlogs': 0,
        'eligible_departments': 'Computer Science, Information Technology, Electronics',
        'deadline': today + timedelta(days=15),
    },
    {
        'company': 'Infosys Limited',
        'title': 'Digital Specialist Engineer',
        'description': 'Work on Infosys Digital products and help enterprises modernize their legacy systems. You\'ll build microservices, APIs, and data pipelines. Strong knowledge of Python, Node.js, Docker preferred.',
        'location': 'Mysuru / Chennai',
        'package': '6.5',
        'job_type': 'Full Time',
        'min_cgpa': 7.5,
        'max_backlogs': 0,
        'eligible_departments': 'Computer Science, Information Technology',
        'deadline': today + timedelta(days=1),  # Closing tomorrow — urgency!
    },
    {
        'company': 'Infosys Limited',
        'title': 'Software Engineer Intern',
        'description': 'A 6-month internship at Infosys innovation labs. Work on real projects in Agile sprints alongside senior engineers. Stipend + potential Pre-Placement Offer.',
        'location': 'Bengaluru',
        'package': '15000/month',
        'job_type': 'Internship',
        'min_cgpa': 6.0,
        'max_backlogs': 2,
        'eligible_departments': 'Computer Science, Information Technology, Electronics, Mechanical',
        'deadline': today + timedelta(days=30),
    },
    # TCS
    {
        'company': 'Tata Consultancy Services',
        'title': 'Assistant System Engineer',
        'description': 'TCS invites fresh graduates to join as ASE (Assistant System Engineer). Selected candidates go through the TCS Digital and Ninja tracks. Extensive training on in-demand technologies is provided over 3 months.',
        'location': 'Pan India',
        'package': '3.6',
        'job_type': 'Full Time',
        'min_cgpa': 6.0,
        'max_backlogs': 0,
        'eligible_departments': 'Computer Science, Information Technology, Electronics, Electrical',
        'deadline': today + timedelta(days=10),
    },
    {
        'company': 'Tata Consultancy Services',
        'title': 'TCS Digital — Full Stack Developer',
        'description': 'TCS Digital track for high-performing candidates. Work on React, Node.js, microservices, and cloud platforms. Higher package for proven aptitude through TCS NQT Digital test.',
        'location': 'Bengaluru / Mumbai / Kolkata',
        'package': '7.0',
        'job_type': 'Full Time',
        'min_cgpa': 7.0,
        'max_backlogs': 0,
        'eligible_departments': 'Computer Science, Information Technology',
        'deadline': today + timedelta(days=0),  # Closing TODAY — urgent!
    },
    # Wipro
    {
        'company': 'Wipro Technologies',
        'title': 'Project Engineer',
        'description': 'Wipro Project Engineer role involves working with global clients across banking, retail and telecom domains. Training on SAP, Salesforce, and cloud technologies provided. Strong communication skills required.',
        'location': 'Bengaluru / Hyderabad / Pune',
        'package': '3.5',
        'job_type': 'Full Time',
        'min_cgpa': 6.0,
        'max_backlogs': 1,
        'eligible_departments': 'Computer Science, Information Technology, Electronics, Mechanical',
        'deadline': today + timedelta(days=8),
    },
    {
        'company': 'Wipro Technologies',
        'title': 'Wipro Turbo — Elite Engineer',
        'description': 'Wipro Turbo program for top-performing students. Fast-track career with higher salary band, exclusive projects, and leadership mentoring. Requires clearing Wipro Elite NTH test.',
        'location': 'Bengaluru',
        'package': '6.5',
        'job_type': 'Full Time',
        'min_cgpa': 7.5,
        'max_backlogs': 0,
        'eligible_departments': 'Computer Science, Information Technology',
        'deadline': today + timedelta(days=20),
    },
    # Cognizant
    {
        'company': 'Cognizant Technology Solutions',
        'title': 'Programmer Analyst Trainee',
        'description': 'Cognizant PAT program brings fresh engineers into a 3-month classroom training followed by on-the-job coaching. Domains: Java EE, .NET, Python, Salesforce, AI/ML. Strong problem-solving skills required.',
        'location': 'Chennai / Pune / Bengaluru / Hyderabad',
        'package': '4.5',
        'job_type': 'Full Time',
        'min_cgpa': 6.0,
        'max_backlogs': 0,
        'eligible_departments': 'Computer Science, Information Technology, Electronics',
        'deadline': today + timedelta(days=18),
    },
    # Accenture
    {
        'company': 'Accenture India',
        'title': 'Software Development Engineer',
        'description': 'Accenture SDE role focuses on delivering technology projects for Fortune 500 clients. Work with Java, Python, cloud (AWS/Azure/GCP), and DevOps tools. Excellent learning culture with Accenture certifications.',
        'location': 'Bengaluru / Mumbai / Hyderabad / Pune',
        'package': '4.5',
        'job_type': 'Full Time',
        'min_cgpa': 6.5,
        'max_backlogs': 0,
        'eligible_departments': 'Computer Science, Information Technology',
        'deadline': today + timedelta(days=25),
    },
    {
        'company': 'Accenture India',
        'title': 'Technology Analyst Intern',
        'description': '6-month internship at Accenture Applied Intelligence division. Work on data science, NLP, and ML pipelines for enterprise clients. Python, pandas, scikit-learn experience preferred.',
        'location': 'Bengaluru',
        'package': '20000/month',
        'job_type': 'Internship',
        'min_cgpa': 7.0,
        'max_backlogs': 1,
        'eligible_departments': 'Computer Science, Information Technology, Electronics',
        'deadline': today + timedelta(days=12),
    },
    # Amazon
    {
        'company': 'Amazon Development Centre',
        'title': 'SDE-1 (Software Development Engineer)',
        'description': 'Amazon SDE-1 is a highly competitive role for bright engineering graduates. You will work on Amazon\'s global platforms serving millions of customers. Requires strong DSA fundamentals, system design basics, and leadership principles.',
        'location': 'Hyderabad / Bengaluru',
        'package': '26.0',
        'job_type': 'Full Time',
        'min_cgpa': 8.0,
        'max_backlogs': 0,
        'eligible_departments': 'Computer Science, Information Technology',
        'deadline': today + timedelta(days=7),
    },
]

created_jobs = []
for j in JOBS:
    company = created_companies.get(j['company'])
    if not company:
        print(f"  ! Skipping job (company not found): {j['company']}")
        continue

    job, created_job = JobRequirement.objects.get_or_create(
        company=company,
        title=j['title'],
        defaults={
            'description': j['description'],
            'location': j['location'],
            'package': j['package'],
            'job_type': j['job_type'],
            'min_cgpa': j['min_cgpa'],
            'max_backlogs': j['max_backlogs'],
            'eligible_departments': j['eligible_departments'],
            'deadline': j['deadline'],
        }
    )
    created_jobs.append(job)
    status = "NEW" if created_job else "exists"
    days_left = (j['deadline'] - today).days
    deadline_label = "TODAY ⚠️" if days_left == 0 else (f"tomorrow ⚠️" if days_left == 1 else f"in {days_left} days")
    print(f"  ✓ [{status}] Job: {job.title} @ {company.name} — Deadline {deadline_label}")

# ──────────────────────────────────────────────────────────────────────────────
# 5. NOTIFICATIONS for all existing students
# ──────────────────────────────────────────────────────────────────────────────
students = Student.objects.all()
notif_count = 0

for student in students:
    for job in created_jobs:
        days_left = (job.deadline - today).days
        if days_left >= 0:
            msg = f"🏢 New Opportunity: {job.title} at {job.company.name} — Package: ₹{job.package} LPA | Deadline: {job.deadline.strftime('%d %b %Y')}"
            already_exists = Notification.objects.filter(student=student, message=msg).exists()
            if not already_exists:
                Notification.objects.create(student=student, message=msg)
                notif_count += 1

print(f"\n✓ Created {notif_count} notifications for {students.count()} student(s)")

# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("  ✅  SEED COMPLETE — JSS Portal is now populated!")
print("="*60)
print("\nCompany Login Credentials (all companies):")
print("  Password: Company@123")
for c in COMPANIES:
    print(f"  Username: {c['username']}  →  {c['name']}")
print("\nPlacement Officer:")
print("  Username: placement_officer  |  Password: Officer@123")
print("="*60)
