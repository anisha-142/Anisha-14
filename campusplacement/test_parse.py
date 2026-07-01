from django.template.loader import get_template
try:
    get_template('index.html')
    print("SUCCESS")
except Exception as e:
    print("FAILED", e)
