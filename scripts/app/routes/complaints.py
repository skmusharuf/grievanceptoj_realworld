"""Complaint submission and tracking routes"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models.complaint import (
    submit_complaint, get_complaint_by_id_and_email,
    get_complaint_status_history
)
from app.models.database import get_db_connection
from app.models.otp import verify_tracking_otp
from app.services.classification import classify_complaint_gemini
from app.services.translation import translate_to_english
from app.services.email_service import send_email
from app.config import EMAIL_USER, EMAIL_PASSWORD

bp = Blueprint('complaints', __name__, url_prefix='/api/complaints')

@bp.route('/submit', methods=['POST'])
def submit_complaint_route():
    """Submit a new complaint with zone assignment"""
    try:
        data = request.json
        
        print(f"[v0] Received complaint submission request")
        
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        aadhar = data.get('aadhar')
        description = data.get('description')
        full_address = data.get('full_address', '')
        area_id = data.get('area_id')
        
        if not description:
            return jsonify({'error': 'Description is required'}), 400

        description = translate_to_english(description)

        if not all([name, email, description]):
            return jsonify({'error': 'Name, email, and description are required'}), 400
        
        # Get zone and circle info from area
        zone_id = None
        circle_id = None
        locality_name = None
        zone_name = None
        
        if area_id:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT a.zone_id, a.circle_id, a.area_name, z.zone_name
                FROM areas a
                JOIN zones z ON z.id = a.zone_id
                WHERE a.id = ?
            ''', (area_id,))
            
            area_info = cursor.fetchone()
            if area_info:
                zone_id = area_info['zone_id']
                circle_id = area_info['circle_id']
                locality_name = area_info['area_name']
                zone_name = area_info['zone_name']
            
            conn.close()
        
        # Classify using Gemini
        print(f"[v0] Classifying complaint using Gemini...")
        category, criticality = classify_complaint_gemini(description)
        
        # Submit complaint
        complaint_id, otp = submit_complaint(
            name, email, phone, aadhar, description,
            full_address, area_id, zone_id, circle_id, locality_name,
            category, criticality
        )
        
        # Send confirmation email
        subject = "Complaint Submitted Successfully - Grievance Hub"
        body = f"""
Hello {name},

Your complaint has been submitted successfully!

Complaint Details:
------------------
Complaint ID: {complaint_id}
Category: {category}
Criticality: {criticality}
Status: Pending
Zone: {zone_name or 'Not Assigned'}
Locality: {locality_name or 'Not Specified'}

Your tracking OTP is: {otp}

Use this Complaint ID and OTP to track your complaint status.

You will receive email updates when the status of your complaint changes.

Thank you for using Grievance Hub.

Best regards,
Grievance Hub Team
Hyderabad Municipal Corporation
        """
        
        send_email(email, subject, body)
        
        print(f"[v0] New complaint: {complaint_id} | Zone: {zone_id} | Category: {category}")
        
        response = {
            'success': True,
            'complaint_id': complaint_id,
            'category': category,
            'criticality': criticality,
            'zone': zone_name,
            'locality': locality_name,
            'message': 'Complaint submitted successfully'
        }
        
        if not EMAIL_USER or not EMAIL_PASSWORD:
            response['otp'] = otp
        
        return jsonify(response)
    
    except Exception as e:
        print(f"[v0] ERROR submitting complaint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@bp.route('/track', methods=['POST'])
def track_complaint():
    """Track complaint with OTP verification"""
    try:
        data = request.json
        complaint_id = data.get('complaint_id')
        email = data.get('email')
        otp = data.get('otp')
        
        if not all([complaint_id, email, otp]):
            return jsonify({'error': 'Complaint ID, email, and OTP are required'}), 400
        
        # Verify OTP
        if not verify_tracking_otp(complaint_id, email, otp):
            return jsonify({'error': 'Invalid OTP'}), 401
        
        # Get complaint with zone info
        complaint = get_complaint_by_id_and_email(complaint_id, email)
        
        if not complaint:
            return jsonify({'error': 'Complaint not found'}), 404
        
        # Get status history
        history = get_complaint_status_history(complaint['id'])
        
        return jsonify({
            'success': True,
            'complaint': {
                'id': complaint['complaint_id'],
                'name': complaint['name'],
                'email': complaint['email'],
                'phone': complaint['phone'],
                'description': complaint['description'],
                'full_address': complaint['full_address'],
                'locality_name': complaint['locality_name'],
                'zone_name': complaint['zone_name'],
                'zone_number': complaint['zone_number'],
                'circle_name': complaint['circle_name'],
                'category': complaint['category'],
                'criticality': complaint['criticality'],
                'status': complaint['status'],
                'created_at': complaint['created_at'],
                'updated_at': complaint['updated_at'],
                'resolved_at': complaint['resolved_at']
            },
            'history': history
        })
    
    except Exception as e:
        print(f"[v0] Error tracking complaint: {e}")
        return jsonify({'error': str(e)}), 500
