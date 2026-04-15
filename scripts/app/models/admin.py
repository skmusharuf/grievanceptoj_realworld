"""Admin model - database operations for admins"""

import hashlib
import uuid
from datetime import datetime, timedelta
from app.models.database import get_db_connection

def verify_admin_credentials(email, password):
    """Verify admin email and password"""
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT a.*, z.zone_name, c.circle_name
        FROM admins a
        LEFT JOIN zones z ON z.id = a.zone_id
        LEFT JOIN circles c ON c.id = a.circle_id
        WHERE a.email = ? AND a.password_hash = ? AND a.is_active = 1
    ''', (email, password_hash))
    
    admin = cursor.fetchone()
    conn.close()
    
    return admin

def create_admin_session(admin_id):
    """Create a new admin session"""
    session_token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(hours=24)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO admin_sessions (session_token, admin_id, expires_at)
        VALUES (?, ?, ?)
    ''', (session_token, admin_id, expires_at.isoformat()))
    
    conn.commit()
    conn.close()
    
    return session_token

def verify_admin_session(session_token):
    """Verify admin session and return admin info"""
    if not session_token:
        return None
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT a.*, z.zone_name, c.circle_name, s.expires_at
        FROM admin_sessions s
        JOIN admins a ON a.id = s.admin_id
        LEFT JOIN zones z ON z.id = a.zone_id
        LEFT JOIN circles c ON c.id = a.circle_id
        WHERE s.session_token = ? AND s.is_active = 1
    ''', (session_token,))
    
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        return None
    
    # Check expiration
    if result['expires_at']:
        expires = datetime.fromisoformat(result['expires_at'])
        if datetime.now() > expires:
            return None
    
    return dict(result)

def logout_admin_session(session_token):
    """Invalidate admin session"""
    if session_token:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE admin_sessions SET is_active = 0 WHERE session_token = ?
        ''', (session_token,))
        
        conn.commit()
        conn.close()
