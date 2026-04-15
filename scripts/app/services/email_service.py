"""Email service for sending emails"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD, EMAIL_FROM

def send_email(to_email, subject, body):
    """Send email using SMTP"""
    try:
        if not EMAIL_USER or not EMAIL_PASSWORD:
            print(f"[v0] Email not configured. Email would be sent to: {to_email}")
            print(f"[v0] Subject: {subject}")
            return False
        
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Fix: Add timeout and proper error handling
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT, timeout=10)
        server.starttls()
        
        # Strip whitespace from password (common issue with .env files)
        password = EMAIL_PASSWORD.strip() if isinstance(EMAIL_PASSWORD, str) else EMAIL_PASSWORD
        server.login(EMAIL_USER.strip(), password)
        
        text = msg.as_string()
        server.sendmail(EMAIL_FROM, to_email, text)
        server.quit()
        
        print(f"[v0] Email sent successfully to {to_email}")
        return True
    
    except smtplib.SMTPAuthenticationError as e:
        print(f"[v0] Email Authentication Error: Check your EMAIL_USER and EMAIL_PASSWORD in .env")
        print(f"[v0] If using Gmail, use App Password (https://myaccount.google.com/apppasswords)")
        print(f"[v0] Error: {e}")
        return False
    
    except smtplib.SMTPException as e:
        print(f"[v0] SMTP Error: {e}")
        return False
    
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
    
    zone_name = complaint.get('zone_name', 'N/A')
    admin_id = admin_info.get('admin_id', 'N/A') if admin_info else 'N/A'
    department = complaint.get('category', 'N/A')
    
    body = f"""
Hello {complaint['name']},

{status_messages[new_status]['message']}

Complaint Details:
------------------
Complaint ID: {complaint['complaint_id']}
Department: {department}
Zone: {zone_name}
Admin ID: {admin_id}
Status: {new_status}
Locality: {complaint.get('locality_name', 'N/A')}

If you have any questions, please contact our support team.

Thank you,
Grievance Hub Team
Hyderabad Municipal Corporation
    """
    
    return send_email(
        complaint['email'],
        status_messages[new_status]['subject'],
        body
    )
