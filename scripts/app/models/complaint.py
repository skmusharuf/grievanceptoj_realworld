"""Complaint model - database operations for complaints"""

from datetime import datetime, timedelta
from app.models.database import get_db_connection
from app.utils.helpers import generate_complaint_id, generate_otp

def submit_complaint(name, email, phone, aadhar, description, full_address, area_id, zone_id, circle_id, locality_name, category, criticality):
    """Submit a new complaint to database"""
    complaint_id = generate_complaint_id()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO complaints (
            complaint_id, name, email, phone, aadhar, description,
            full_address, area_id, zone_id, circle_id, locality_name,
            category, criticality, status, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pending', ?, ?)
    ''', (
        complaint_id, name, email, phone, aadhar, description,
        full_address, area_id, zone_id, circle_id, locality_name,
        category, criticality, datetime.now().isoformat(), datetime.now().isoformat()
    ))
    
    complaint_db_id = cursor.lastrowid
    
    # Generate tracking OTP
    otp = generate_otp()
    expires_at = datetime.now() + timedelta(days=30)
    
    cursor.execute('''
        INSERT INTO otp_storage (identifier, otp, otp_type, expires_at)
        VALUES (?, ?, 'tracking', ?)
    ''', (f"{complaint_id}:{email}", otp, expires_at.isoformat()))
    
    # Log initial status
    cursor.execute('''
        INSERT INTO complaint_status_history (complaint_id, old_status, new_status, notes)
        VALUES (?, NULL, 'Pending', 'Complaint submitted')
    ''', (complaint_db_id,))
    
    conn.commit()
    conn.close()
    
    return complaint_id, otp

def get_complaint_by_id_and_email(complaint_id, email):
    """Get complaint with zone info"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT c.*, z.zone_name, z.zone_number, ci.circle_name
        FROM complaints c
        LEFT JOIN zones z ON z.id = c.zone_id
        LEFT JOIN circles ci ON ci.id = c.circle_id
        WHERE c.complaint_id = ? AND c.email = ?
    ''', (complaint_id, email))
    
    complaint = cursor.fetchone()
    conn.close()
    
    return complaint

def get_complaint_status_history(complaint_db_id):
    """Get status history for a complaint"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM complaint_status_history
        WHERE complaint_id = ?
        ORDER BY created_at DESC
    ''', (complaint_db_id,))
    
    history = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return history

def get_admin_complaints(admin, department=None, status=None, zone_filter=None):
    """Get complaints based on admin's role and zone"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build query based on admin role
    query = '''
        SELECT c.*, z.zone_name, z.zone_number, ci.circle_name,
               a.name as assigned_admin_name
        FROM complaints c
        LEFT JOIN zones z ON z.id = c.zone_id
        LEFT JOIN circles ci ON ci.id = c.circle_id
        LEFT JOIN admins a ON a.id = c.assigned_admin_id
        WHERE 1=1
    '''
    params = []
    
    # Role-based filtering
    if admin['role'] == 'department_admin':
        # Department admin can only see complaints in their circle
        query += ' AND c.circle_id = ?'
        params.append(admin['circle_id'])
    elif admin['role'] == 'sub_admin':
        # Sub admin can see all complaints in their zone
        query += ' AND c.zone_id = ?'
        params.append(admin['zone_id'])
    # Super admin can see all complaints
    
    # Additional filters
    if department and department != 'all':
        query += ' AND c.category = ?'
        params.append(department)
    
    if status and status != 'all':
        query += ' AND c.status = ?'
        params.append(status)
    
    if zone_filter and zone_filter != 'all' and admin['role'] == 'super_admin':
        query += ' AND c.zone_id = ?'
        params.append(int(zone_filter))
    
    query += ' ORDER BY c.created_at DESC'
    
    cursor.execute(query, params)
    
    complaints = []
    for row in cursor.fetchall():
        complaints.append({
            'id': row['complaint_id'],
            'db_id': row['id'],
            'name': row['name'],
            'email': row['email'],
            'phone': row['phone'],
            'description': row['description'],
            'full_address': row['full_address'],
            'locality_name': row['locality_name'],
            'zone_id': row['zone_id'],
            'zone_name': row['zone_name'],
            'zone_number': row['zone_number'],
            'circle_name': row['circle_name'],
            'category': row['category'],
            'criticality': row['criticality'],
            'status': row['status'],
            'assigned_admin_name': row['assigned_admin_name'],
            'created_at': row['created_at'],
            'updated_at': row['updated_at'],
            'resolved_at': row['resolved_at']
        })
    
    conn.close()
    return complaints

def get_complaint_by_id(complaint_id):
    """Get complaint by complaint_id"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT c.*, z.zone_name FROM complaints c
        LEFT JOIN zones z ON z.id = c.zone_id
        WHERE c.complaint_id = ?
    ''', (complaint_id,))
    
    complaint = cursor.fetchone()
    conn.close()
    
    return complaint

def update_complaint_status(complaint_id, complaint_db_id, new_status, admin_id, notes=''):
    """Update complaint status"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get old status
    cursor.execute('SELECT status FROM complaints WHERE complaint_id = ?', (complaint_id,))
    old_status = cursor.fetchone()['status']
    
    resolved_at = datetime.now().isoformat() if new_status == 'Resolved' else None
    
    # Update complaint
    cursor.execute('''
        UPDATE complaints
        SET status = ?, updated_at = ?, resolved_at = ?, assigned_admin_id = ?
        WHERE complaint_id = ?
    ''', (new_status, datetime.now().isoformat(), resolved_at, admin_id, complaint_id))
    
    # Log status change
    cursor.execute('''
        INSERT INTO complaint_status_history 
        (complaint_id, old_status, new_status, changed_by_admin_id, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', (complaint_db_id, old_status, new_status, admin_id, notes))
    
    conn.commit()
    conn.close()
    
    return old_status
