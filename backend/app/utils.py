import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime, timedelta
import json
import re
import google.generativeai as genai
from googletrans import Translator

translator = Translator()

# Gemini configuration
genai.configure(api_key=os.getenv('GEMINI_API_KEY', ''))
MODEL_NAME = "gemini-2.5-flash"

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

def generate_complaint_id():
    """Generate unique complaint ID"""
    return 'CMP' + ''.join(random.choices(string.digits, k=8))

def generate_otp():
    """Generate 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))

def generate_admin_id():
    """Generate unique admin ID"""
    return 'ADM' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def translate_to_english(text):
    """Translate Hindi/Telugu complaints to English automatically"""
    try:
        translated = translator.translate(text, dest='en')
        print(f"[v0] Translated to English: {translated.text}")
        return translated.text
    except Exception as e:
        print(f"[v0] Translation error: {e}")
        return text

def classify_complaint_with_gemini(description):
    """Classify complaint using Gemini LLM"""
    try:
        description = translate_to_english(description)
        
        if not description or len(description) < 3:
            return {
                "category": "Invalid",
                "criticality": "None"
            }
        
        prompt = GEMINI_PROMPT.replace("<<<USER_COMPLAINT>>>", description)
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        text_response = response.text.strip()
        print("[v0] Gemini raw response:\n", text_response)
        
        match = re.search(r'\{[\s\S]*\}', text_response)
        if match:
            result = json.loads(match.group())
            category = result.get("department", "General")
            criticality = result.get("criticality", "Non-Critical")
        else:
            category = "General"
            criticality = "Non-Critical"
        
        return {
            "category": category,
            "criticality": criticality
        }
    
    except Exception as e:
        print(f"[v0] Error classifying complaint: {e}")
        return {
            "category": "General",
            "criticality": "Non-Critical"
        }

def send_email(to_email, subject, body):
    """Send email using SMTP"""
    try:
        EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
        EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
        EMAIL_USER = os.getenv('EMAIL_USER', '')
        EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
        EMAIL_FROM = os.getenv('EMAIL_FROM', EMAIL_USER)
        
        if not EMAIL_USER or not EMAIL_PASSWORD:
            print(f"[v0] Email not configured. Email would be sent to: {to_email}")
            print(f"[v0] Subject: {subject}")
            return False
        
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_FROM, to_email, text)
        server.quit()
        
        print(f"[v0] Email sent successfully to {to_email}")
        return True
    
    except Exception as e:
        print(f"[v0] Error sending email: {e}")
        return False

def send_status_update_email(complaint, new_status, admin_info=None):
    """Send email notification when complaint status changes"""
    status_messages = {
        'In Progress': {
            'subject': 'Your Complaint is Being Processed - Grievance Hub',
            'message': 'Our technicians will reach your location soon to address your complaint.'
        },
        'Resolved': {
            'subject': 'Your Complaint Has Been Resolved - Grievance Hub',
            'message': 'Your complaint has been successfully resolved. Thank you for your patience.'
        }
    }
    
    if new_status not in status_messages:
        return False
    
    zone_name = complaint.zone.zone_name if complaint.zone else 'N/A'
    admin_id = admin_info.get('admin_id', 'N/A') if admin_info else 'N/A'
    department = complaint.category or 'N/A'
    
    body = f"""
Hello {complaint.name},

{status_messages[new_status]['message']}

Complaint Details:
------------------
Complaint ID: {complaint.complaint_id}
Department: {department}
Zone: {zone_name}
Admin ID: {admin_id}
Status: {new_status}
Locality: {complaint.locality_name or 'N/A'}

If you have any questions, please contact our support team.

Thank you,
Grievance Hub Team
Hyderabad Municipal Corporation
    """
    
    return send_email(
        complaint.email,
        status_messages[new_status]['subject'],
        body
    )

CATEGORIES = [
    "CM Office (Miscellaneous)",
    "Development Authority",
    "Municipal",
    "Police",
    "Public Works Department",
    "Transport",
    "General"
]
