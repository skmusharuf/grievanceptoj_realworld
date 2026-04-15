"""Authentication routes"""

from flask import Blueprint, request, jsonify
from app.models.otp import store_auth_otp, verify_auth_otp
from app.models.admin import verify_admin_credentials, create_admin_session
from app.services.email_service import send_email
from app.config import EMAIL_USER, EMAIL_PASSWORD

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/send-otp', methods=['POST'])
def send_otp():
    """Send OTP to email for verification"""
    try:
        data = request.json
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        otp = store_auth_otp(email)
        
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
        
        if not EMAIL_USER or not EMAIL_PASSWORD:
            response['otp'] = otp
            response['message'] = 'OTP generated (email not configured - check console)'
        
        return jsonify(response)
    
    except Exception as e:
        print(f"[v0] Error sending OTP: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    """Verify OTP for email"""
    try:
        data = request.json
        email = data.get('email')
        otp = data.get('otp')
        
        if not all([email, otp]):
            return jsonify({'error': 'Email and OTP are required'}), 400
        
        if not verify_auth_otp(email, otp):
            return jsonify({'error': 'Invalid OTP'}), 401
        
        print(f"[v0] OTP verified successfully for {email}")
        
        return jsonify({
            'success': True,
            'message': 'OTP verified successfully'
        })
    
    except Exception as e:
        print(f"[v0] Error verifying OTP: {e}")
        return jsonify({'error': str(e)}), 500
