from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.extensions import db
from app.models.otp_storage import OTPStorage
from app.config import Config

auth_bp = Blueprint('auth', __name__)

# In-memory OTP storage for auth (temporary fallback)
auth_otp_storage = {}


def generate_otp():
    """Generate 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))


def send_email(to_email, subject, body):
    """Send email using SMTP"""
    try:
        if not Config.EMAIL_USER or not Config.EMAIL_PASSWORD:
            print(f"[v0] Email not configured. Email would be sent to: {to_email}")
            print(f"[v0] Subject: {subject}")
            return False

        msg = MIMEMultipart()
        msg['From'] = Config.EMAIL_FROM
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(Config.EMAIL_HOST, Config.EMAIL_PORT)
        server.starttls()
        server.login(Config.EMAIL_USER, Config.EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(Config.EMAIL_FROM, to_email, text)
        server.quit()

        print(f"[v0] Email sent successfully to {to_email}")
        return True

    except Exception as e:
        print(f"[v0] Error sending email: {e}")
        return False


@auth_bp.route('/send-otp', methods=['POST'])
def send_otp():
    """Send OTP to email for verification"""
    try:
        data = request.json
        email = data.get('email')

        if not email:
            return jsonify({'error': 'Email is required'}), 400

        otp = generate_otp()
        auth_otp_storage[email] = otp

        # Also store in database
        expires_at = datetime.now() + timedelta(minutes=10)

        existing = OTPStorage.query.filter_by(identifier=email).first()
        if existing:
            existing.otp = otp
            existing.otp_type = 'auth'
            existing.expires_at = expires_at
            existing.is_used = 0
        else:
            new_otp = OTPStorage(
                identifier=email,
                otp=otp,
                otp_type='auth',
                expires_at=expires_at
            )
            db.session.add(new_otp)

        db.session.commit()

        subject = "Your Grievance System OTP"
        body = f"""
Hello,

Your OTP for the Grievance System is: {otp}

This OTP is valid for 10 minutes.

If you did not request this OTP, please ignore this email.

Thank you,
Grievance System Team
        """

        email_sent = send_email(email, subject, body)

        print(f"[v0] OTP generated for {email}: {otp}")

        response = {
            'success': True,
            'message': 'OTP sent successfully'
        }

        if not Config.EMAIL_USER or not Config.EMAIL_PASSWORD:
            response['otp'] = otp
            response['message'] = 'OTP generated (email not configured - check console)'

        return jsonify(response)

    except Exception as e:
        print(f"[v0] Error sending OTP: {e}")
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    """Verify OTP for email"""
    try:
        data = request.json
        email = data.get('email')
        otp = data.get('otp')

        if not all([email, otp]):
            return jsonify({'error': 'Email and OTP are required'}), 400

        stored_otp = auth_otp_storage.get(email)

        if not stored_otp:
            return jsonify({'error': 'OTP not found or expired'}), 404

        if stored_otp != otp:
            return jsonify({'error': 'Invalid OTP'}), 401

        del auth_otp_storage[email]

        print(f"[v0] OTP verified successfully for {email}")

        return jsonify({
            'success': True,
            'message': 'OTP verified successfully'
        })

    except Exception as e:
        print(f"[v0] Error verifying OTP: {e}")
        return jsonify({'error': str(e)}), 500
