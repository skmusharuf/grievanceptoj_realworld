from flask import Blueprint, request, jsonify
from app import db
from app.models import Complaint, ComplaintStatusHistory, OTPStorage, Area, Zone, Circle
from app.utils import (
    generate_complaint_id, generate_otp, classify_complaint_with_gemini,
    send_email, CATEGORIES
)
from datetime import datetime, timedelta

bp = Blueprint('complaints', __name__, url_prefix='/api/complaints')

@bp.route('/submit', methods=['POST'])
def submit_complaint():
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

        if not all([name, email, description]):
            return jsonify({'error': 'Name, email, and description are required'}), 400
        
        # Get zone and circle info from area
        zone_id = None
        circle_id = None
        locality_name = None
        zone_name = None
        
        if area_id:
            area = Area.query.get(area_id)
            if area:
                zone_id = area.zone_id
                circle_id = area.circle_id
                locality_name = area.area_name
                zone_name = area.zone.zone_name
        
        # Classify using Gemini
        print(f"[v0] Classifying complaint using Gemini...")
        classification = classify_complaint_with_gemini(description)
        category = classification.get("category", "General")
        criticality = classification.get("criticality", "Non-Critical")
        
        complaint_id = generate_complaint_id()
        
        # Save to database
        complaint = Complaint(
            complaint_id=complaint_id,
            name=name,
            email=email,
            phone=phone,
            aadhar=aadhar,
            description=description,
            full_address=full_address,
            area_id=area_id,
            zone_id=zone_id,
            circle_id=circle_id,
            locality_name=locality_name,
            category=category,
            criticality=criticality,
            status='Pending'
        )
        
        db.session.add(complaint)
        db.session.flush()
        
        # Generate tracking OTP
        otp = generate_otp()
        expires_at = datetime.utcnow() + timedelta(days=30)
        
        otp_record = OTPStorage(
            identifier=f"{complaint_id}:{email}",
            otp=otp,
            otp_type='tracking',
            expires_at=expires_at
        )
        db.session.add(otp_record)
        
        # Log initial status
        status_history = ComplaintStatusHistory(
            complaint_id=complaint.id,
            old_status=None,
            new_status='Pending',
            notes='Complaint submitted'
        )
        db.session.add(status_history)
        
        db.session.commit()
        
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
        
        # Include OTP if email is not configured
        import os
        EMAIL_USER = os.getenv('EMAIL_USER', '')
        EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
        if not EMAIL_USER or not EMAIL_PASSWORD:
            response['otp'] = otp
        
        return jsonify(response)
    
    except Exception as e:
        print(f"[v0] ERROR submitting complaint: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
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
        otp_record = OTPStorage.query.filter_by(
            identifier=f"{complaint_id}:{email}",
            otp_type='tracking'
        ).first()
        
        if not otp_record or otp_record.otp != otp:
            return jsonify({'error': 'Invalid OTP'}), 401
        
        # Get complaint with zone info
        complaint = Complaint.query.filter_by(
            complaint_id=complaint_id,
            email=email
        ).first()
        
        if not complaint:
            return jsonify({'error': 'Complaint not found'}), 404
        
        # Get status history
        history = ComplaintStatusHistory.query.filter_by(
            complaint_id=complaint.id
        ).order_by(ComplaintStatusHistory.created_at.desc()).all()
        
        history_data = [item.to_dict() for item in history]
        
        return jsonify({
            'success': True,
            'complaint': complaint.to_dict(),
            'history': history_data
        })
    
    except Exception as e:
        print(f"[v0] Error tracking complaint: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/classify', methods=['POST'])
def classify_complaint():
    """Classify complaint using Gemini LLM"""
    try:
        data = request.json
        description = data.get('description', '').strip()
        
        if not description or len(description) < 3:
            return jsonify({
                "category": "Invalid",
                "criticality": "None",
                "success": True
            }), 200
        
        classification = classify_complaint_with_gemini(description)
        
        return jsonify({
            "category": classification.get("category", "Invalid"),
            "criticality": classification.get("criticality", "None"),
            "success": True
        }), 200
    
    except Exception as e:
        print(f"[v0] Error in classification: {e}")
        return jsonify({
            "category": "Invalid",
            "criticality": "None",
            "success": False
        }), 500

@bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all complaint categories"""
    return jsonify({
        'success': True,
        'categories': CATEGORIES
    })
