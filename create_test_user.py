import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusplacement.settings')
django.setup()

from django.contrib.auth.models import User
from placement_app.models import Student, College

# Create or get college
college, created = College.objects.get_or_create(
    code='TEST001',
    defaults={
        'name': 'Test College',
        'address': 'Test Address',
        'email': 'test@college.com',
        'phone': '1234567890'
    }
)
if created:
    print(f"✓ Created college: {college.name}")
else:
    print(f"✓ Using existing college: {college.name}")

# Create user
user, created = User.objects.get_or_create(
    username='mr',
    defaults={
        'email': 'mr@campus.com',
        'first_name': 'Mr',
        'last_name': 'Test'
    }
)
if created:
    user.set_password('MrPassword123')
    user.save()
    print(f"✓ Created user: {user.username}")
else:
    print(f"✓ User already exists: {user.username}")

# Create corresponding Student record
student, created = Student.objects.get_or_create(
    user=user,
    defaults={
        'college': college,
        'registration_number': 'STU001',
        'department': 'Computer Science',
        'course': 'B.Tech',
        'year': 3,
        'cgpa': 8.5,
        'percentage_10th': 90.0,
        'percentage_12th': 92.0,
    }
)
if created:
    print(f"✓ Created Student record for user: {user.username}")
else:
    print(f"✓ Student record already exists for user: {user.username}")

print(f"\n=== LOGIN CREDENTIALS ===")
print(f"Username: mr")
print(f"Password: MrPassword123")
print(f"========================")
