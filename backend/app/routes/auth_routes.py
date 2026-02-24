from flask import Blueprint, request, jsonify
from app import db
from app.models import Admin, AdminSession, OTPStorage
from app.utils import generate_otp, send_email
from datetime import datetime, timedelta
import uuid
import os

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# In-memory OTP storage for quick access
auth_otp_storage = {}

@bp.route('/send-otp', methods=['POST'])
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
        expires_at = datetime.utcnow() + timedelta(minutes=10)
        
        otp_record = OTPStorage.query.filter_by(identifier=email, otp_type='auth').first()
        if otp_record:
            otp_record.otp = otp
            otp_record.expires_at = expires_at
            otp_record.is_used = False
        else:
            otp_record = OTPStorage(
                identifier=email,
                otp=otp,
                otp_type='auth',
                expires_at=expires_at
            )
            db.session.add(otp_record)
        
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
        
        EMAIL_USER = os.getenv('EMAIL_USER', '')
        EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
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
        
        stored_otp = auth_otp_storage.get(email)
        
        if not stored_otp:
            # Check database
            otp_record = OTPStorage.query.filter_by(
                identifier=email,
                otp_type='auth'
            ).first()
            
            if not otp_record or otp_record.is_used:
                return jsonify({'error': 'OTP not found or expired'}), 404
            
            if otp_record.expires_at and datetime.utcnow() > otp_record.expires_at:
                return jsonify({'error': 'OTP expired'}), 401
            
            if otp_record.otp != otp:
                return jsonify({'error': 'Invalid OTP'}), 401
            
            otp_record.is_used = True
            db.session.commit()
        else:
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

@bp.route('/admin/login', methods=['POST'])
def admin_login():
    """Admin login with role-based access"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        admin = Admin.query.filter_by(email=email, is_active=True).first()
        
        if not admin or not admin.verify_password(password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Create session
        session_token = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(hours=24)
        
        session = AdminSession(
            session_token=session_token,
            admin_id=admin.id,
            expires_at=expires_at
        )
        
        db.session.add(session)
        db.session.commit()
        
        print(f"[v0] Admin login successful: {email} (Role: {admin.role})")
        
        return jsonify({
            'success': True,
            'session_token': session_token,
            'admin': admin.to_dict(),
            'message': 'Login successful'
        })
    
    except Exception as e:
        print(f"[v0] Error in admin login: {e}")
        return jsonify({'error': str(e)}), 500

def verify_admin_session(session_token):
    """Verify admin session and return admin info"""
    if not session_token:
        return None
    
    session = AdminSession.query.filter_by(
        session_token=session_token,
        is_active=True
    ).first()
    
    if not session:
        return None
    
    # Check expiration
    if session.expires_at and datetime.utcnow() > session.expires_at:
        return None
    
    admin = Admin.query.get(session.admin_id)
    if not admin:
        return None
    
    return admin
