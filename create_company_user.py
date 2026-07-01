"""
============================================================
  JSS Placement Portal — Company User Setup Script
  Run with:  python create_company_user.py
============================================================
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusplacement.settings')
django.setup()

from django.contrib.auth.models import User
from placement_app.models import Company, College, PlacementOfficer

# ── 1. List all existing company users ──────────────────────
print("\n" + "="*55)
print("  EXISTING COMPANY USERS IN DATABASE")
print("="*55)

companies = Company.objects.select_related('user').all()
if companies.exists():
    for c in companies:
        print(f"  Username : {c.user.username}")
        print(f"  Company  : {c.name}")
        print(f"  HR Name  : {c.hr_name}")
        print(f"  Email    : {c.user.email}")
        print(f"  Active   : {c.user.is_active}")
        print("-"*55)
    print(f"  Total company accounts: {companies.count()}")
else:
    print("  No company users found in the database.")

# ── 2. Create a test company user if none exist ─────────────
print("\n" + "="*55)
print("  CREATE TEST COMPANY USER")
print("="*55)

TEST_USERNAME = "testcompany"
TEST_PASSWORD = "Company@123"
TEST_EMAIL    = "testcompany@jss.edu"
COMPANY_NAME  = "TCS (Test)"

if User.objects.filter(username=TEST_USERNAME).exists():
    print(f"  User '{TEST_USERNAME}' already exists.")
    user = User.objects.get(username=TEST_USERNAME)
    # Reset password just in case
    user.set_password(TEST_PASSWORD)
    user.save()
    print(f"  Password reset to: {TEST_PASSWORD}")
else:
    user = User.objects.create_user(
        username=TEST_USERNAME,
        email=TEST_EMAIL,
        password=TEST_PASSWORD
    )
    print(f"  Created Django user: {TEST_USERNAME}")

# Check/create Company profile
if not Company.objects.filter(user=user).exists():
    # Need at least one College for PlacementOfficer (optional for Company)
    company = Company.objects.create(
        user=user,
        name=COMPANY_NAME,
        website="https://www.tcs.com",
        description="Test company for development purposes.",
        hr_name="HR Manager",
        hr_email=TEST_EMAIL,
        hr_phone="9876543210",
    )
    print(f"  Created Company profile: {COMPANY_NAME}")
else:
    print(f"  Company profile already exists for '{TEST_USERNAME}'")

print("\n" + "="*55)
print("  LOGIN CREDENTIALS FOR COMPANY DASHBOARD")
print("="*55)
print(f"  URL      : http://127.0.0.1:8000/company-login/")
print(f"  Username : {TEST_USERNAME}")
print(f"  Password : {TEST_PASSWORD}")
print("="*55 + "\n")
