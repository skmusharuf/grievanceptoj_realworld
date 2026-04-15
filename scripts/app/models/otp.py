"""OTP model - database operations for OTP storage"""

from datetime import datetime, timedelta
from app.models.database import get_db_connection
from app.utils.helpers import generate_otp

# In-memory OTP storage for auth (temporary)
auth_otp_storage = {}

def store_auth_otp(email):
    """Generate and store OTP for auth"""
    otp = generate_otp()
    auth_otp_storage[email] = otp
    
    # Also store in database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    expires_at = datetime.now() + timedelta(minutes=10)
    
    cursor.execute('''
        INSERT OR REPLACE INTO otp_storage (identifier, otp, otp_type, expires_at)
        VALUES (?, ?, 'auth', ?)
    ''', (email, otp, expires_at.isoformat()))
    
    conn.commit()
    conn.close()
    
    return otp

def verify_auth_otp(email, otp):
    """Verify OTP for email"""
    stored_otp = auth_otp_storage.get(email)
    
    if not stored_otp:
        return False
    
    if stored_otp != otp:
        return False
    
    del auth_otp_storage[email]
    return True

def verify_tracking_otp(complaint_id, email, otp):
    """Verify tracking OTP"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT otp FROM otp_storage
        WHERE identifier = ? AND otp_type = 'tracking'
    ''', (f"{complaint_id}:{email}",))
    
    otp_record = cursor.fetchone()
    conn.close()
    
    if not otp_record:
        return False
    
    return otp_record['otp'] == otp
