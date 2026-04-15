"""Admin management and dashboard routes"""

from flask import Blueprint, request, jsonify
from app.models.admin import (
    verify_admin_credentials, create_admin_session,
    verify_admin_session, logout_admin_session
)
from app.models.complaint import (
    get_admin_complaints, get_complaint_by_id,
    update_complaint_status
)
from app.services.email_service import send_status_update_email

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@bp.route('/login', methods=['POST'])
def admin_login():
    """Admin login with role-based access"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        admin = verify_admin_credentials(email, password)
        
        if not admin:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Create session
        session_token = create_admin_session(admin['id'])
        
        print(f"[v0] Admin login successful: {email} (Role: {admin['role']})")
        
        return jsonify({
            'success': True,
            'session_token': session_token,
            'admin': {
                'id': admin['id'],
                'admin_id': admin['admin_id'],
                'email': admin['email'],
                'name': admin['name'],
                'role': admin['role'],
                'department': admin['department'],
                'zone_id': admin['zone_id'],
                'zone_name': admin['zone_name'],
                'circle_id': admin['circle_id'],
                'circle_name': admin['circle_name']
            },
            'message': 'Login successful'
        })
    
    except Exception as e:
        print(f"[v0] Error in admin login: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/complaints', methods=['GET'])
def get_complaints():
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
        
        complaints = get_admin_complaints(admin, department, status, zone_filter)
        
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

@bp.route('/complaints/<complaint_id>/status', methods=['PUT'])
def update_status(complaint_id):
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
        complaint = get_complaint_by_id(complaint_id)
        
        if not complaint:
            return jsonify({'error': 'Complaint not found'}), 404
        
        # Check if already resolved - cannot change
        if complaint['status'] == 'Resolved':
            return jsonify({'error': 'Cannot modify resolved complaints'}), 403
        
        # Check admin's permission based on role
        if admin['role'] == 'department_admin':
            if complaint['circle_id'] != admin['circle_id']:
                return jsonify({'error': 'Not authorized to modify this complaint'}), 403
        elif admin['role'] == 'sub_admin':
            if complaint['zone_id'] != admin['zone_id']:
                return jsonify({'error': 'Not authorized to modify this complaint'}), 403
        
        # Update status
        old_status = update_complaint_status(complaint_id, complaint['id'], new_status, admin['id'], notes)
        
        # Send email notification
        complaint_dict = dict(complaint)
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
        return jsonify({'error': str(e)}), 500

@bp.route('/logout', methods=['POST'])
def logout():
    """Admin logout - invalidate session"""
    try:
        session_token = request.headers.get('X-Session-Token')
        logout_admin_session(session_token)
        
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        })
    
    except Exception as e:
        print(f"[v0] Error in logout: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/profile', methods=['GET'])
def get_profile():
    """Get current admin's profile"""
    try:
        session_token = request.headers.get('X-Session-Token')
        
        admin = verify_admin_session(session_token)
        if not admin:
            return jsonify({'error': 'Unauthorized'}), 401
        
        return jsonify({
            'success': True,
            'admin': {
                'id': admin['id'],
                'admin_id': admin['admin_id'],
                'email': admin['email'],
                'name': admin['name'],
                'phone': admin['phone'],
                'role': admin['role'],
                'department': admin['department'],
                'zone_id': admin['zone_id'],
                'zone_name': admin['zone_name'],
                'circle_id': admin['circle_id'],
                'circle_name': admin['circle_name']
            }
        })
    
    except Exception as e:
        print(f"[v0] Error getting profile: {e}")
        return jsonify({'error': str(e)}), 500
