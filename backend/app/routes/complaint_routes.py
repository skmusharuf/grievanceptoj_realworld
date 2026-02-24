from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import random
import string
import json
import re
from app.extensions import db
from app.models.complaint import Complaint
from app.models.complaint_status_history import ComplaintStatusHistory
from app.models.otp_storage import OTPStorage
from app.models.area import Area
from app.models.zone import Zone
from app.models.circle import Circle
from app.config import Config
from app.routes.auth_routes import send_email

complaint_bp = Blueprint('complaint', __name__)

# Gemini AI prompt for classification
GEMINI_PROMPT = """
You are an intelligent grievance classification assistant for a citizen complaint management system.

You will receive a text complaint written in English (sometimes with small grammar or spelling errors).

Your tasks:
1. Identify the correct department that should handle it. Choose ONLY from:
   - CM Office (Miscellaneous)
   - Development Authority
   - Municipal
   - Police
   - Public Works Department
   - Transport
2. Determine whether the complaint is **Critical** or **Non-Critical**.
   - Critical means urgent or safety-related (accidents, fires, injuries, harassment, violence, death, etc.).
   - Non-Critical means routine issues (garbage, water, road maintenance, paperwork delays, etc.).
3. Return ONLY valid JSON in this exact format:
{
  "department": "<one of the 6 departments>",
  "criticality": "<Critical or Non-Critical>",
  "confidence_reason": "<short reason for your decision>"
}

If the input is unclear, meaningless, or too short to classify, return:
{
  "department": "Invalid",
  "criticality": "None",
  "confidence_reason": "Complaint not clear or incomplete"
}

Now classify the following complaint:
<<<USER_COMPLAINT>>>
"""


def generate_complaint_id():
    """Generate unique complaint ID"""
    return 'CMP' + ''.join(random.choices(string.digits, k=8))


def generate_otp():
    """Generate 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))


def translate_to_english(text):
    """Translate Hindi/Telugu complaints to English automatically"""
    try:
        from googletrans import Translator
        translator = Translator()
        translated = translator.translate(text, dest='en')
        print(f"[v0] Translated to English: {translated.text}")
        return translated.text
    except Exception as e:
        print(f"[v0] Translation error (using original text): {e}")
        return text


def classify_with_gemini(description):
    """Classify complaint using Gemini LLM"""
    try:
        import google.generativeai as genai
        genai.configure(api_key=Config.GEMINI_API_KEY)

        prompt = GEMINI_PROMPT.replace("<<<USER_COMPLAINT>>>", description)
        model = genai.GenerativeModel(Config.GEMINI_MODEL)
        response = model.generate_content(prompt)
        text_response = response.text.strip()
        print(f"\nGemini raw response:\n{text_response}")

        match = re.search(r'\{[\s\S]*\}', text_response)
        if match:
            result = json.loads(match.group())
            category = result.get("department", "General")
            criticality = result.get("criticality", "Non-Critical")
            return category, criticality

        return "General", "Non-Critical"

    except Exception as e:
        print(f"[v0] Gemini classification failed: {e}")
        return "General", "Non-Critical"


def send_status_update_email(complaint_dict, new_status, admin_info=None):
    """Send email notification when complaint status changes"""
    status_messages = {
        'In Progress': {
            'subject': 'Your Complaint is Being Processed - Grievance Hub',
            'message': 'Our technicians will reach your location soon to address your complaint.'
        },
        'Resolved': {
            'subject': 'Your Complaint Has Been Resolved - Grievance Hub',
            'message': 'Your complaint has been successfully resolved. Thank you for your patience.'
        }
    }

    if new_status not in status_messages:
        return False

    zone_name = complaint_dict.get('zone_name', 'N/A')
    admin_id = admin_info.get('admin_id', 'N/A') if admin_info else 'N/A'
    department = complaint_dict.get('category', 'N/A')

    body = f"""
Hello {complaint_dict['name']},

{status_messages[new_status]['message']}

Complaint Details:
------------------
Complaint ID: {complaint_dict['complaint_id']}
Department: {department}
Zone: {zone_name}
Admin ID: {admin_id}
Status: {new_status}
Locality: {complaint_dict.get('locality_name', 'N/A')}

If you have any questions, please contact our support team.

Thank you,
Grievance Hub Team
Hyderabad Municipal Corporation
    """

    return send_email(
        complaint_dict['email'],
        status_messages[new_status]['subject'],
        body
    )


@complaint_bp.route('/classify', methods=['POST'])
def classify_complaint():
    """Classify complaint using Gemini LLM"""
    try:
        data = request.json
        description = data.get('description', '').strip()
        description = translate_to_english(description)

        if not description or len(description) < 3:
            return jsonify({
                "category": "Invalid",
                "criticality": "None",
                "success": True
            }), 200

        category, criticality = classify_with_gemini(description)

        return jsonify({
            "category": category,
            "criticality": criticality,
            "success": True
        }), 200

    except Exception as e:
        print(f"Error in classification: {e}")
        return jsonify({
            "category": "Invalid",
            "criticality": "None",
            "success": False
        }), 500


@complaint_bp.route('/submit', methods=['POST'])
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

        description = translate_to_english(description)

        if not all([name, email, description]):
            return jsonify({'error': 'Name, email, and description are required'}), 400

        # Get zone and circle info from area
        zone_id = None
        circle_id = None
        locality_name = None
        zone_name = None

        if area_id:
            area = db.session.query(
                Area.zone_id, Area.circle_id, Area.area_name, Zone.zone_name
            ).join(Zone, Zone.id == Area.zone_id) \
             .filter(Area.id == area_id) \
             .first()

            if area:
                zone_id = area.zone_id
                circle_id = area.circle_id
                locality_name = area.area_name
                zone_name = area.zone_name

        # Classify using Gemini
        print(f"[v0] Classifying complaint using Gemini...")
        category, criticality = classify_with_gemini(description)

        complaint_id = generate_complaint_id()

        # Save to database
        new_complaint = Complaint(
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
        db.session.add(new_complaint)
        db.session.flush()  # Get the ID

        # Generate tracking OTP
        otp = generate_otp()
        expires_at = datetime.now() + timedelta(days=30)

        tracking_otp = OTPStorage(
            identifier=f"{complaint_id}:{email}",
            otp=otp,
            otp_type='tracking',
            expires_at=expires_at
        )
        db.session.add(tracking_otp)

        # Log initial status
        status_log = ComplaintStatusHistory(
            complaint_id=new_complaint.id,
            old_status=None,
            new_status='Pending',
            notes='Complaint submitted'
        )
        db.session.add(status_log)

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

        if not Config.EMAIL_USER or not Config.EMAIL_PASSWORD:
            response['otp'] = otp

        return jsonify(response)

    except Exception as e:
        print(f"[v0] ERROR submitting complaint: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@complaint_bp.route('/track', methods=['POST'])
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
        complaint = db.session.query(
            Complaint,
            Zone.zone_name,
            Zone.zone_number,
            Circle.circle_name
        ).outerjoin(Zone, Zone.id == Complaint.zone_id) \
         .outerjoin(Circle, Circle.id == Complaint.circle_id) \
         .filter(Complaint.complaint_id == complaint_id, Complaint.email == email) \
         .first()

        if not complaint:
            return jsonify({'error': 'Complaint not found'}), 404

        c = complaint[0]

        # Get status history
        history = ComplaintStatusHistory.query.filter_by(
            complaint_id=c.id
        ).order_by(ComplaintStatusHistory.created_at.desc()).all()

        history_list = []
        for h in history:
            history_list.append({
                'id': h.id,
                'old_status': h.old_status,
                'new_status': h.new_status,
                'notes': h.notes,
                'created_at': h.created_at.isoformat() if h.created_at else None
            })

        return jsonify({
            'success': True,
            'complaint': {
                'id': c.complaint_id,
                'name': c.name,
                'email': c.email,
                'phone': c.phone,
                'description': c.description,
                'full_address': c.full_address,
                'locality_name': c.locality_name,
                'zone_name': complaint.zone_name,
                'zone_number': complaint.zone_number,
                'circle_name': complaint.circle_name,
                'category': c.category,
                'criticality': c.criticality,
                'status': c.status,
                'created_at': c.created_at.isoformat() if c.created_at else None,
                'updated_at': c.updated_at.isoformat() if c.updated_at else None,
                'resolved_at': c.resolved_at.isoformat() if c.resolved_at else None
            },
            'history': history_list
        })

    except Exception as e:
        print(f"[v0] Error tracking complaint: {e}")
        return jsonify({'error': str(e)}), 500
