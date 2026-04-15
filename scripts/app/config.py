"""
Configuration and constants for the Grievance System
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_PATH = 'data/grievance.db'

# Email configuration
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USER = os.getenv('EMAIL_USER', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
EMAIL_FROM = os.getenv('EMAIL_FROM', EMAIL_USER)

# AI/ML Configuration
MODEL_NAME = "gemini-2.5-flash"
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# Constants
VALID_STATUSES = ['Pending', 'In Progress', 'Resolved']
VALID_ROLES = ['super_admin', 'sub_admin', 'department_admin']

DEPARTMENTS = [
    "CM Office (Miscellaneous)",
    "Development Authority",
    "Municipal",
    "Police",
    "Public Works Department",
    "Transport",
    "General"
]

GEMINI_PROMPT = """
You are an intelligent grievance classification assistant for a citizen complaint management system.

You will receive a text complaint written in English (sometimes with small grammar or spelling errors).

Your tasks:
1. Identify the correct department that should handle it. Choose ONLY from:
   - CM Office (Miscellaneous)
   - Development Authority
   - Municipal
   - Police
   - Public Works Department
   - Transport
2. Determine whether the complaint is **Critical** or **Non-Critical**.
   - Critical means urgent or safety-related (accidents, fires, injuries, harassment, violence, death, etc.).
   - Non-Critical means routine issues (garbage, water, road maintenance, paperwork delays, etc.).
3. Return ONLY valid JSON in this exact format:
{
  "department": "<one of the 6 departments>",
  "criticality": "<Critical or Non-Critical>",
  "confidence_reason": "<short reason for your decision>"
}

If the input is unclear, meaningless, or too short to classify, return:
{
  "department": "Invalid",
  "criticality": "None",
  "confidence_reason": "Complaint not clear or incomplete"
}

Now classify the following complaint:
<<<USER_COMPLAINT>>>
"""

# Print email configuration on startup
def log_email_config():
    """Log email configuration status"""
    print("\n" + "="*50)
    print("EMAIL CONFIGURATION")
    print("="*50)
    print(f"EMAIL_HOST: {EMAIL_HOST}")
    print(f"EMAIL_PORT: {EMAIL_PORT}")
    print(f"EMAIL_USER: {EMAIL_USER}")
    print(f"EMAIL_PASSWORD: {'*' * len(EMAIL_PASSWORD) if EMAIL_PASSWORD else '(NOT SET)'}")
    print(f"EMAIL_FROM: {EMAIL_FROM}")
    if EMAIL_USER and EMAIL_PASSWORD:
        print("Email is CONFIGURED - emails will be sent")
    else:
        print("Email is NOT CONFIGURED - OTPs will only print to console")
    print("="*50 + "\n")
