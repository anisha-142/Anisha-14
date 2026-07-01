"""
Django management command to create a test company user.

Usage:
    python manage.py create_company_user

Options:
    --username   Username for the company user  (default: testcompany)
    --password   Password for the company user  (default: Company@123)
    --name       Company name                   (default: TCS - Test Company)
    --list       List all existing company users
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from placement_app.models import Company


class Command(BaseCommand):
    help = "Create a test company user or list existing company users"

    def add_arguments(self, parser):
        parser.add_argument('--username', default='testcompany',  help='Username (default: testcompany)')
        parser.add_argument('--password', default='Company@123',  help='Password  (default: Company@123)')
        parser.add_argument('--name',     default='TCS - Test Company', help='Company name')
        parser.add_argument('--list',     action='store_true',    help='List all existing company users')

    def handle(self, *args, **options):
        self.stdout.write("")

        # ── LIST mode ───────────────────────────────────────────────
        if options['list']:
            companies = Company.objects.select_related('user').all()
            if not companies.exists():
                self.stdout.write(self.style.WARNING("  No company users found in the database."))
                self.stdout.write(self.style.NOTICE("  Run:  python manage.py create_company_user\n"))
                return

            self.stdout.write(self.style.SUCCESS("=" * 55))
            self.stdout.write(self.style.SUCCESS("  EXISTING COMPANY USERS"))
            self.stdout.write(self.style.SUCCESS("=" * 55))
            for c in companies:
                self.stdout.write(f"  Username : {c.user.username}")
                self.stdout.write(f"  Company  : {c.name}")
                self.stdout.write(f"  HR Name  : {c.hr_name}")
                self.stdout.write(f"  Active   : {c.user.is_active}")
                self.stdout.write("-" * 55)
            self.stdout.write(f"  Total: {companies.count()} company account(s)\n")
            return

        # ── CREATE mode ─────────────────────────────────────────────
        username = options['username']
        password = options['password']
        name     = options['name']

        self.stdout.write(self.style.SUCCESS("=" * 55))
        self.stdout.write(self.style.SUCCESS("  CREATING COMPANY USER"))
        self.stdout.write(self.style.SUCCESS("=" * 55))

        # Get or create the Django User
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.WARNING(f"  User '{username}' already existed — password reset."))
        else:
            user = User.objects.create_user(
                username=username,
                email=f"{username}@jss.edu",
                password=password,
            )
            self.stdout.write(self.style.SUCCESS(f"  ✓ Created Django user: {username}"))

        # Get or create the Company profile
        if Company.objects.filter(user=user).exists():
            company = Company.objects.get(user=user)
            self.stdout.write(self.style.WARNING(f"  Company profile '{company.name}' already exists."))
        else:
            Company.objects.create(
                user=user,
                name=name,
                website="https://example.com",
                description="Test company created for development.",
                hr_name="HR Manager",
                hr_email=f"{username}@jss.edu",
                hr_phone="9876543210",
            )
            self.stdout.write(self.style.SUCCESS(f"  ✓ Created Company profile: {name}"))

        # Print credentials
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("=" * 55))
        self.stdout.write(self.style.SUCCESS("  LOGIN CREDENTIALS"))
        self.stdout.write(self.style.SUCCESS("=" * 55))
        self.stdout.write(f"  URL      :  http://127.0.0.1:8000/company-login/")
        self.stdout.write(f"  Username :  {username}")
        self.stdout.write(f"  Password :  {password}")
        self.stdout.write(self.style.SUCCESS("=" * 55))
        self.stdout.write("")
