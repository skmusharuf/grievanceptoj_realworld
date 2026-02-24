from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import hashlib
import uuid
from app.extensions import db
from app.models.admin import Admin
from app.models.admin_session import AdminSession
from app.models.complaint import Complaint
from app.models.complaint_status_history import ComplaintStatusHistory
from app.models.zone import Zone
from app.models.circle import Circle
from app.routes.complaint_routes import send_status_update_email

admin_bp = Blueprint('admin', __name__)


def verify_admin_session(session_token):
    """Verify admin session and return admin info"""
    if not session_token:
        return None

    result = db.session.query(
        Admin, Zone.zone_name, Circle.circle_name, AdminSession.expires_at
    ).join(AdminSession, AdminSession.admin_id == Admin.id) \
     .outerjoin(Zone, Zone.id == Admin.zone_id) \
     .outerjoin(Circle, Circle.id == Admin.circle_id) \
     .filter(AdminSession.session_token == session_token, AdminSession.is_active == 1) \
     .first()

    if not result:
        return None

    admin, zone_name, circle_name, expires_at = result

    # Check expiration
    if expires_at and datetime.now() > expires_at:
        return None

    return {
        'id': admin.id,
        'admin_id': admin.admin_id,
        'email': admin.email,
        'name': admin.name,
        'phone': admin.phone,
        'role': admin.role,
        'department': admin.department,
        'zone_id': admin.zone_id,
        'zone_name': zone_name,
        'circle_id': admin.circle_id,
        'circle_name': circle_name
    }


@admin_bp.route('/login', methods=['POST'])
def admin_login():
    """Admin login with role-based access"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        result = db.session.query(
            Admin, Zone.zone_name, Circle.circle_name
        ).outerjoin(Zone, Zone.id == Admin.zone_id) \
         .outerjoin(Circle, Circle.id == Admin.circle_id) \
         .filter(Admin.email == email, Admin.password_hash == password_hash, Admin.is_active == 1) \
         .first()

        if not result:
            return jsonify({'error': 'Invalid email or password'}), 401

        admin, zone_name, circle_name = result

        # Create session
        session_token = str(uuid.uuid4())
        expires_at = datetime.now() + timedelta(hours=24)

        new_session = AdminSession(
            session_token=session_token,
            admin_id=admin.id,
            expires_at=expires_at
        )
        db.session.add(new_session)
        db.session.commit()

        print(f"[v0] Admin login successful: {email} (Role: {admin.role})")

        return jsonify({
            'success': True,
            'session_token': session_token,
            'admin': {
                'id': admin.id,
                'admin_id': admin.admin_id,
                'email': admin.email,
                'name': admin.name,
                'role': admin.role,
                'department': admin.department,
                'zone_id': admin.zone_id,
                'zone_name': zone_name,
                'circle_id': admin.circle_id,
                'circle_name': circle_name
            },
            'message': 'Login successful'
        })

    except Exception as e:
        print(f"[v0] Error in admin login: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/complaints', methods=['GET'])
def get_admin_complaints():
    """Get complaints based on admin's role and zone"""
    try:
        session_token = request.headers.get('X-Session-Token') or request.args.get('session_token')

        admin = verify_admin_session(session_token)
        if not admin:
            return jsonify({'error': 'Unauthorized: Invalid or missing session token'}), 401

        # Get filter parameters
        department = request.args.get('department')
        status = request.args.get('status', 'all')
        zone_filter = request.args.get('zone')

        # Build query
        query = db.session.query(
            Complaint,
            Zone.zone_name,
            Zone.zone_number,
            Circle.circle_name,
            Admin.name.label('assigned_admin_name')
        ).outerjoin(Zone, Zone.id == Complaint.zone_id) \
         .outerjoin(Circle, Circle.id == Complaint.circle_id) \
         .outerjoin(Admin, Admin.id == Complaint.assigned_admin_id)

        # Role-based filtering
        if admin['role'] == 'department_admin':
            query = query.filter(Complaint.circle_id == admin['circle_id'])
        elif admin['role'] == 'sub_admin':
            query = query.filter(Complaint.zone_id == admin['zone_id'])
        # Super admin can see all complaints

        # Additional filters
        if department and department != 'all':
            query = query.filter(Complaint.category == department)

        if status and status != 'all':
            query = query.filter(Complaint.status == status)

        if zone_filter and zone_filter != 'all' and admin['role'] == 'super_admin':
            query = query.filter(Complaint.zone_id == int(zone_filter))

        query = query.order_by(Complaint.created_at.desc())

        results = query.all()

        complaints = []
        for row in results:
            c = row[0]
            complaints.append({
                'id': c.complaint_id,
                'db_id': c.id,
                'name': c.name,
                'email': c.email,
                'phone': c.phone,
                'description': c.description,
                'full_address': c.full_address,
                'locality_name': c.locality_name,
                'zone_id': c.zone_id,
                'zone_name': row.zone_name,
                'zone_number': row.zone_number,
                'circle_name': row.circle_name,
                'category': c.category,
                'criticality': c.criticality,
                'status': c.status,
                'assigned_admin_name': row.assigned_admin_name,
                'created_at': c.created_at.isoformat() if c.created_at else None,
                'updated_at': c.updated_at.isoformat() if c.updated_at else None,
                'resolved_at': c.resolved_at.isoformat() if c.resolved_at else None
            })

        # Calculate statistics
        total = len(complaints)
        pending = len([c for c in complaints if c['status'] == 'Pending'])
        in_progress = len([c for c in complaints if c['status'] == 'In Progress'])
        resolved = len([c for c in complaints if c['status'] == 'Resolved'])
        critical = len([c for c in complaints if c.get('criticality') == 'Critical'])

        return jsonify({
            'success': True,
            'complaints': complaints,
            'admin_info': {
                'role': admin['role'],
                'zone_name': admin['zone_name'],
                'circle_name': admin['circle_name'],
                'department': admin['department']
            },
            'statistics': {
                'total': total,
                'pending': pending,
                'in_progress': in_progress,
                'resolved': resolved,
                'critical': critical
            }
        })

    except Exception as e:
        print(f"[v0] Error fetching complaints: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/complaints/<complaint_id>/status', methods=['PUT'])
def update_complaint_status(complaint_id):
    """Update complaint status with restriction for resolved complaints"""
    try:
        data = request.json or {}
        session_token = request.headers.get('X-Session-Token') or data.get('session_token')
        new_status = data.get('status')
        notes = data.get('notes', '')

        admin = verify_admin_session(session_token)
        if not admin:
            return jsonify({'error': 'Unauthorized: Invalid or missing session token'}), 401

        if not new_status:
            return jsonify({'error': 'Status is required'}), 400

        if new_status not in ['Pending', 'In Progress', 'Resolved']:
            return jsonify({'error': 'Invalid status'}), 400

        # Get current complaint
        complaint_result = db.session.query(
            Complaint, Zone.zone_name
        ).outerjoin(Zone, Zone.id == Complaint.zone_id) \
         .filter(Complaint.complaint_id == complaint_id) \
         .first()

        if not complaint_result:
            return jsonify({'error': 'Complaint not found'}), 404

        complaint, zone_name = complaint_result

        # Check if already resolved - cannot change
        if complaint.status == 'Resolved':
            return jsonify({'error': 'Cannot modify resolved complaints'}), 403

        # Check admin's permission based on role
        if admin['role'] == 'department_admin':
            if complaint.circle_id != admin['circle_id']:
                return jsonify({'error': 'Not authorized to modify this complaint'}), 403
        elif admin['role'] == 'sub_admin':
            if complaint.zone_id != admin['zone_id']:
                return jsonify({'error': 'Not authorized to modify this complaint'}), 403

        old_status = complaint.status
        resolved_at = datetime.now() if new_status == 'Resolved' else None

        # Update complaint
        complaint.status = new_status
        complaint.updated_at = datetime.now()
        complaint.resolved_at = resolved_at
        complaint.assigned_admin_id = admin['id']

        # Log status change
        status_log = ComplaintStatusHistory(
            complaint_id=complaint.id,
            old_status=old_status,
            new_status=new_status,
            changed_by_admin_id=admin['id'],
            notes=notes
        )
        db.session.add(status_log)

        db.session.commit()

        # Send email notification
        complaint_dict = {
            'name': complaint.name,
            'email': complaint.email,
            'complaint_id': complaint.complaint_id,
            'category': complaint.category,
            'locality_name': complaint.locality_name,
            'zone_name': zone_name
        }
        send_status_update_email(complaint_dict, new_status, admin)

        print(f"[v0] Status updated: {complaint_id} -> {new_status} by {admin['email']}")

        return jsonify({
            'success': True,
            'message': 'Status updated successfully',
            'old_status': old_status,
            'new_status': new_status
        })

    except Exception as e:
        print(f"[v0] Error updating status: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/logout', methods=['POST'])
def admin_logout():
    """Admin logout - invalidate session"""
    try:
        session_token = request.headers.get('X-Session-Token')

        if session_token:
            session = AdminSession.query.filter_by(session_token=session_token).first()
            if session:
                session.is_active = 0
                db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        })

    except Exception as e:
        print(f"[v0] Error in logout: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/profile', methods=['GET'])
def get_admin_profile():
    """Get current admin's profile"""
    try:
        session_token = request.headers.get('X-Session-Token')

        admin = verify_admin_session(session_token)
        if not admin:
            return jsonify({'error': 'Unauthorized'}), 401

        return jsonify({
            'success': True,
            'admin': admin
        })

    except Exception as e:
        print(f"[v0] Error getting profile: {e}")
        return jsonify({'error': str(e)}), 500
