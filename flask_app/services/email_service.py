"""
Email service for sending OTPs and notifications
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app


def send_email(to_email, subject, body):
    """Send email using SMTP"""
    try:
        config = current_app.config
        email_user = config.get('EMAIL_USER', '')
        email_password = config.get('EMAIL_PASSWORD', '')
        email_host = config.get('EMAIL_HOST', 'smtp.gmail.com')
        email_port = config.get('EMAIL_PORT', 587)
        email_from = config.get('EMAIL_FROM', email_user)

        if not email_user or not email_password:
            print(f"[GrievanceHub] Email not configured. Would send to: {to_email}")
            print(f"[GrievanceHub] Subject: {subject}")
            return False

        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(email_host, email_port)
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_from, to_email, msg.as_string())
        server.quit()

        print(f"[GrievanceHub] Email sent to {to_email}")
        return True

    except Exception as e:
        print(f"[GrievanceHub] Email error: {e}")
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
