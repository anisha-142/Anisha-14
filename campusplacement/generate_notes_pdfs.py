import os
import sys

def generate_notes():
    # Make sure fpdf is installed
    try:
        from fpdf import FPDF
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "fpdf"])
        from fpdf import FPDF

    class StudyNotesPDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.set_text_color(100, 116, 139)
            self.cell(0, 10, 'JSS Campus Placement Portal | Study Vault', 0, 1, 'R')
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(148, 163, 184)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

        def doc_title(self, label):
            self.set_font('Arial', 'B', 24)
            self.set_text_color(30, 41, 59)
            self.cell(0, 15, label, 0, 1, 'L')
            self.ln(5)

        def section_heading(self, label):
            self.set_font('Arial', 'B', 14)
            self.set_text_color(79, 70, 229)
            self.cell(0, 10, label, 0, 1, 'L')
            self.ln(2)

        def text_paragraph(self, text):
            self.set_font('Arial', '', 11)
            self.set_text_color(51, 65, 85)
            # Safe latin-1 conversion
            safe_text = text.encode('latin-1', 'replace').decode('latin-1')
            self.multi_cell(0, 6, safe_text)
            self.ln(4)

    # 1. PHP Programming Complete Guide.pdf
    pdf = StudyNotesPDF()
    pdf.add_page()
    pdf.doc_title("PHP Programming: Complete Placement Guide")
    pdf.section_heading("1. Introduction to PHP")
    pdf.text_paragraph(
        "PHP (Hypertext Preprocessor) is a widely-used open source general-purpose scripting language that is especially "
        "suited for web development and can be embedded into HTML. PHP runs on the server side, meaning the code is executed "
        "on the server, and the plain HTML output is sent back to the browser."
    )
    pdf.section_heading("2. Core Concepts & Syntax")
    pdf.text_paragraph(
        "- Variables in PHP start with a dollar sign ($) followed by the name (e.g., $txt = 'Hello World';).\n"
        "- PHP is loosely typed: you do not need to declare data types for variables.\n"
        "- Common constructs include echo/print statements, arrays (indexed, associative, and multidimensional), and functions."
    )
    pdf.section_heading("3. Object-Oriented PHP (OOP)")
    pdf.text_paragraph(
        "Modern PHP (PHP 7+) heavily utilizes OOP principles. Classes are templates for objects, defined using the 'class' "
        "keyword. Important OOP features include constructors (__construct), inheritance (extends), access modifiers (public, "
        "protected, private), and namespaces to organize classes into logical groups."
    )
    pdf.section_heading("4. Database Connectivity (PDO)")
    pdf.text_paragraph(
        "PDO (PHP Data Objects) is the modern, secure way to connect to databases in PHP. It supports prepared statements, "
        "which protect applications against SQL Injection vulnerabilities. Example connection code:\n"
        "$conn = new PDO('mysql:host=$host;dbname=$db', $username, $password);\n"
        "$stmt = $conn->prepare('SELECT * FROM users WHERE email = :email');\n"
        "$stmt->execute(['email' => $user_email]);"
    )
    pdf.output("PHP_Programming_Complete_Guide.pdf")
    print("Generated PHP PDF.")

    # 2. Artificial Intelligence and Data Science Fundamentals.pdf
    pdf = StudyNotesPDF()
    pdf.add_page()
    pdf.doc_title("AI & Data Science: Core Fundamentals")
    pdf.section_heading("1. Overview of Artificial Intelligence")
    pdf.text_paragraph(
        "Artificial Intelligence (AI) refers to the simulation of human intelligence processes by machines, especially computer "
        "systems. These processes include learning (information acquisition), reasoning (rules to reach conclusions), and self-correction."
    )
    pdf.section_heading("2. Machine Learning vs. Deep Learning")
    pdf.text_paragraph(
        "- Machine Learning (ML): A subset of AI that provides systems the ability to automatically learn and improve from experience "
        "without being explicitly programmed. ML algorithms are grouped into Supervised (Linear Regression, SVM), Unsupervised (K-Means), "
        "and Reinforcement Learning.\n"
        "- Deep Learning (DL): A specialized subset of ML based on Artificial Neural Networks (ANNs) with multiple layers (deep networks). "
        "DL excels at processing unstructured data like images (CNNs) and sequential text (RNNs, Transformers)."
    )
    pdf.section_heading("3. Data Science Lifecycle")
    pdf.text_paragraph(
        "Data Science combines statistics, mathematics, and computer science to extract insights from data. The key phases include:\n"
        "1. Data Acquisition: Collecting structured/unstructured data.\n"
        "2. Data Cleaning: Handling missing values, outliers, and formatting irregularities.\n"
        "3. Exploratory Data Analysis (EDA): Visualizing data trends using Python libraries like Pandas, Matplotlib, and Seaborn.\n"
        "4. Model Training & Evaluation: Splitting data into training/testing sets, fitting ML algorithms, and scoring performance (Accuracy, F1-Score)."
    )
    pdf.output("Artificial_Intelligence_and_Data_Science_Fundamentals.pdf")
    print("Generated AI PDF.")

    # 3. Digital Marketing and SEO Essentials.pdf
    pdf = StudyNotesPDF()
    pdf.add_page()
    pdf.doc_title("Digital Marketing & SEO Essentials")
    pdf.section_heading("1. What is Digital Marketing?")
    pdf.text_paragraph(
        "Digital marketing, also called online marketing, is the promotion of brands to connect with potential customers "
        "using the internet and other forms of digital communication. This includes search engines, social media, email, "
        "websites, and multimedia messages."
    )
    pdf.section_heading("2. Search Engine Optimization (SEO)")
    pdf.text_paragraph(
        "SEO is the practice of orienting your website to rank higher on a search engine results page (SERP) so that you "
        "receive more organic (non-paid) traffic. The core pillars of SEO are:\n"
        "- On-Page SEO: Optimizing page titles, meta descriptions, headings (H1-H6), and content with target keywords.\n"
        "- Off-Page SEO: Building authority and trust through backlinks from other reputable websites.\n"
        "- Technical SEO: Ensuring fast page load speeds, mobile responsiveness, secure HTTPS protocols, and clean site architecture."
    )
    pdf.section_heading("3. Key Performance Indicators (KPIs)")
    pdf.text_paragraph(
        "To measure digital marketing success, marketers track core metrics:\n"
        "- Click-Through Rate (CTR): Clicked links / Total ad impressions.\n"
        "- Conversion Rate: Action takers (sales, signups) / Total visitors.\n"
        "- Return on Ad Spend (ROAS): Revenue generated / Ad campaign cost.\n"
        "- Cost Per Click (CPC) and Customer Acquisition Cost (CAC)."
    )
    pdf.output("Digital_Marketing_and_SEO_Essentials.pdf")
    print("Generated Marketing PDF.")

if __name__ == "__main__":
    generate_notes()
