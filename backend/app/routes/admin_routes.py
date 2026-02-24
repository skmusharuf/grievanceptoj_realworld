from flask import Blueprint, request, jsonify
from app import db
from app.models import Complaint, Admin, ComplaintStatusHistory
from app.routes.auth_routes import verify_admin_session
from app.utils import send_status_update_email
from datetime import datetime

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def get_admin_from_session(request):
    """Extract and verify admin from session token"""
    session_token = request.headers.get('X-Session-Token') or request.args.get('session_token')
    admin = verify_admin_session(session_token)
    
    if not admin:
        return None, ('Unauthorized: Invalid or missing session token', 401)
    
    return admin, None

@bp.route('/complaints', methods=['GET'])
def get_admin_complaints():
    """Get complaints based on admin's role and zone"""
    try:
        admin, error = get_admin_from_session(request)
        if error:
            return jsonify({'error': error[0]}), error[1]
        
        # Get filter parameters
        department = request.args.get('department')
        status = request.args.get('status', 'all')
        zone_filter = request.args.get('zone')
        
        # Build query based on admin role
        query = Complaint.query
        
        # Role-based filtering
        if admin.role == 'department_admin':
            # Department admin can only see complaints in their circle
            query = query.filter_by(circle_id=admin.circle_id)
        elif admin.role == 'sub_admin':
            # Sub admin can see complaints in their zone
            query = query.filter_by(zone_id=admin.zone_id)
        # super_admin can see all complaints
        
        # Apply additional filters
        if department:
            query = query.filter_by(category=department)
        
        if status != 'all':
            query = query.filter_by(status=status)
        
        if zone_filter:
            query = query.filter_by(zone_id=zone_filter)
        
        complaints = query.order_by(Complaint.created_at.desc()).all()
        
        complaints_data = [complaint.to_dict() for complaint in complaints]
        
        return jsonify({
            'success': True,
            'admin_role': admin.role,
            'complaints': complaints_data,
            'count': len(complaints_data)
        })
    
    except Exception as e:
        print(f"[v0] Error fetching admin complaints: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/complaints/<int:complaint_db_id>/status', methods=['PUT'])
def update_complaint_status(complaint_db_id):
    """Update complaint status by admin"""
    try:
        admin, error = get_admin_from_session(request)
        if error:
            return jsonify({'error': error[0]}), error[1]
        
        complaint = Complaint.query.get(complaint_db_id)
        if not complaint:
            return jsonify({'error': 'Complaint not found'}), 404
        
        # Check authorization based on role
        if admin.role == 'department_admin' and complaint.circle_id != admin.circle_id:
            return jsonify({'error': 'Unauthorized: You can only update complaints in your circle'}), 403
        elif admin.role == 'sub_admin' and complaint.zone_id != admin.zone_id:
            return jsonify({'error': 'Unauthorized: You can only update complaints in your zone'}), 403
        
        data = request.json
        new_status = data.get('status')
        notes = data.get('notes', '')
        
        valid_statuses = ['Pending', 'In Progress', 'Resolved']
        if new_status not in valid_statuses:
            return jsonify({'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'}), 400
        
        old_status = complaint.status
        
        # Update complaint
        complaint.status = new_status
        complaint.updated_at = datetime.utcnow()
        complaint.assigned_admin_id = admin.id
        
        if new_status == 'Resolved':
            complaint.resolved_at = datetime.utcnow()
        
        # Log status change
        status_history = ComplaintStatusHistory(
            complaint_id=complaint.id,
            old_status=old_status,
            new_status=new_status,
            changed_by_admin_id=admin.id,
            notes=notes
        )
        
        db.session.add(status_history)
        db.session.commit()
        
        # Send email notification
        admin_info = {'admin_id': admin.admin_id}
        send_status_update_email(complaint, new_status, admin_info)
        
        print(f"[v0] Complaint {complaint.complaint_id} status updated to {new_status} by {admin.email}")
        
        return jsonify({
            'success': True,
            'complaint_id': complaint.complaint_id,
            'old_status': old_status,
            'new_status': new_status,
            'message': f'Status updated to {new_status}'
        })
    
    except Exception as e:
        print(f"[v0] Error updating complaint status: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/complaints/<int:complaint_db_id>/assign', methods=['PUT'])
def assign_complaint(complaint_db_id):
    """Assign complaint to an admin"""
    try:
        admin, error = get_admin_from_session(request)
        if error:
            return jsonify({'error': error[0]}), error[1]
        
        # Only super_admin and sub_admin can assign complaints
        if admin.role not in ['super_admin', 'sub_admin']:
            return jsonify({'error': 'Unauthorized: Only super admin or sub admin can assign complaints'}), 403
        
        complaint = Complaint.query.get(complaint_db_id)
        if not complaint:
            return jsonify({'error': 'Complaint not found'}), 404
        
        data = request.json
        assign_to_admin_id = data.get('admin_id')
        
        target_admin = Admin.query.get(assign_to_admin_id)
        if not target_admin:
            return jsonify({'error': 'Target admin not found'}), 404
        
        # Verify authorization based on role
        if admin.role == 'sub_admin':
            if complaint.zone_id != admin.zone_id:
                return jsonify({'error': 'You can only assign complaints in your zone'}), 403
            if target_admin.zone_id != admin.zone_id:
                return jsonify({'error': 'Can only assign to admins in your zone'}), 403
        
        old_admin_id = complaint.assigned_admin_id
        complaint.assigned_admin_id = assign_to_admin_id
        
        status_history = ComplaintStatusHistory(
            complaint_id=complaint.id,
            old_status=complaint.status,
            new_status=complaint.status,
            changed_by_admin_id=admin.id,
            notes=f'Assigned to {target_admin.name}'
        )
        
        db.session.add(status_history)
        db.session.commit()
        
        print(f"[v0] Complaint {complaint.complaint_id} assigned to {target_admin.email}")
        
        return jsonify({
            'success': True,
            'complaint_id': complaint.complaint_id,
            'assigned_to': target_admin.to_dict(),
            'message': f'Assigned to {target_admin.name}'
        })
    
    except Exception as e:
        print(f"[v0] Error assigning complaint: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/complaints/<int:complaint_db_id>', methods=['GET'])
def get_complaint_detail(complaint_db_id):
    """Get detailed view of a single complaint"""
    try:
        admin, error = get_admin_from_session(request)
        if error:
            return jsonify({'error': error[0]}), error[1]
        
        complaint = Complaint.query.get(complaint_db_id)
        if not complaint:
            return jsonify({'error': 'Complaint not found'}), 404
        
        # Check authorization
        if admin.role == 'department_admin' and complaint.circle_id != admin.circle_id:
            return jsonify({'error': 'Unauthorized'}), 403
        elif admin.role == 'sub_admin' and complaint.zone_id != admin.zone_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get status history
        history = ComplaintStatusHistory.query.filter_by(
            complaint_id=complaint.id
        ).order_by(ComplaintStatusHistory.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'complaint': complaint.to_dict(),
            'history': [item.to_dict() for item in history]
        })
    
    except Exception as e:
        print(f"[v0] Error fetching complaint detail: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/dashboard-stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics for admin"""
    try:
        admin, error = get_admin_from_session(request)
        if error:
            return jsonify({'error': error[0]}), error[1]
        
        # Build query based on admin role
        query = Complaint.query
        
        if admin.role == 'department_admin':
            query = query.filter_by(circle_id=admin.circle_id)
        elif admin.role == 'sub_admin':
            query = query.filter_by(zone_id=admin.zone_id)
        
        total = query.count()
        pending = query.filter_by(status='Pending').count()
        in_progress = query.filter_by(status='In Progress').count()
        resolved = query.filter_by(status='Resolved').count()
        
        # Category breakdown
        category_stats = {}
        complaints = query.all()
        for complaint in complaints:
            cat = complaint.category or 'Unclassified'
            category_stats[cat] = category_stats.get(cat, 0) + 1
        
        return jsonify({
            'success': True,
            'stats': {
                'total_complaints': total,
                'pending': pending,
                'in_progress': in_progress,
                'resolved': resolved,
                'resolution_rate': (resolved / total * 100) if total > 0 else 0,
                'by_category': category_stats
            }
        })
    
    except Exception as e:
        print(f"[v0] Error fetching dashboard stats: {e}")
        return jsonify({'error': str(e)}), 500
