import os
import subprocess
import sys

def install_and_import(package):
    try:
        import fpdf
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    finally:
        globals()["fpdf"] = __import__(package)

install_and_import('fpdf')
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Campus Placement Portal - Complete Project Analysis', 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        # Handle utf-8 encoding for fpdf
        body = body.encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(0, 6, body)
        self.ln()

pdf = PDF()
pdf.add_page()

# Title Page
pdf.set_font("Arial", "B", 24)
pdf.cell(0, 40, "Project Analysis Report", 0, 1, 'C')
pdf.set_font("Arial", "I", 14)
pdf.cell(0, 10, "Target Project: Campus Placement Portal (Django)", 0, 1, 'C')
pdf.ln(20)

# Slide 1
pdf.chapter_title("1. Project Overview & Structure")
text1 = (
    "The 'Campus Placement Portal' is a comprehensive web application built using the Django framework. "
    "Designed primarily to facilitate the recruitment workflows between Students, Companies, and "
    "Placement Officers/Colleges.\n\n"
    "Key architectural points:\n"
    "- Main App: Contains routing, authentication, and general views (landing, dashboard, resources).\n"
    "- Placement App (placement_app): Encapsulates detailed models and administrative CRUD interfaces.\n"
    "- Multi-Role System: Supports diverse user roles including Students, Companies, and Placement Officers."
)
pdf.chapter_body(text1)

# Slide 2
pdf.chapter_title("2. Core Features & Capabilities")
text2 = (
    "A. User Management & Authentication:\n"
    "   - Custom registration and login flows with email validation and pattern matching for secure passwords.\n"
    "   - Uses Django's built-in User model combined with Role-Based profiles (Student, Company).\n"
    "   - SMTP Integration for welcome emails and login alerts.\n\n"
    "B. Student Dashboard:\n"
    "   - Features a personalized home feed showing application status, notifications, and recommended jobs.\n"
    "   - Access to locked study resources, video tutorials, and practice tests explicitly gated behind authentication.\n\n"
    "C. Corporate Module:\n"
    "   - Dedicated dashboard for companies to post Job Requirements.\n"
    "   - Mechanisms to track total applicants, shortlist candidates, and schedule Interview Rounds."
)
pdf.chapter_body(text2)

# Slide 3
pdf.chapter_title("3. Database & Data Models")
text3 = (
    "The application relies on highly relational data models imported from 'placement_app':\n"
    "- Core Profiles: Student, PlacementOfficer, Company, College.\n"
    "- Recruitment Flow: JobRequirement, JobApplication, InterviewRound, InterviewResult.\n"
    "- Utility: Notification (real-time alerts for student actions).\n\n"
    "Integrations rely heavily on Django's ORM, leveraging complex QuerySets (e.g., filtering recommended jobs based on applied_job_ids and search inputs)."
)
pdf.chapter_body(text3)

# Slide 4
pdf.chapter_title("4. Frontend UI/UX Design")
text4 = (
    "The user interface is built mainly mapped dynamically using the Django Template Language.\n"
    "- Bootstrap integration for responsive, component-driven layouts (cards, modals, badges).\n"
    "- Implementation of asynchronous components like 'ajax-login' and 'ajax-register' for smooth landing page popups.\n"
    "- Advanced Admin Views (e.g., college__view.html) feature aesthetic enhancements such as gradients, hover animations, real-time JavaScript search debouncing, and CSV export functions."
)
pdf.chapter_body(text4)

# Slide 5
pdf.chapter_title("5. Academic Artifacts Observation")
text5 = (
    "The project directory also serves as a comprehensive workspace containing numerous academic resources for a Computer Science/BCA curriculum:\n"
    "- C Programming files (.c, .txt) and slide decks (Decision Making, Loop statements).\n"
    "- DBMS notes, SQL concepts, normalization, transaction controls (many .pdf, .docx files).\n"
    "- Data Structures (binary trees, queues) and basic HTML/CSS notes.\n"
    "This indicates the application is likely an academic major project seamlessly integrating a rigorous theoretical background into a practical software engineering solution."
)
pdf.chapter_body(text5)

output_path = "Project_Analysis_Presentation.pdf"
pdf.output(output_path)
print(f"PDF successfully generated at {os.path.abspath(output_path)}")
