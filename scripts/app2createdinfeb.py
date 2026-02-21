from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os
from datetime import datetime, timedelta
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import json
import hashlib
import uuid
import sqlite3
import google.generativeai as genai
from googletrans import Translator

translator = Translator()

genai.configure(api_key="")
MODEL_NAME = "gemini-2.5-flash"
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

def translate_to_english(text):
    """Translate Hindi/Telugu complaints to English automatically"""
    try:
        translated = translator.translate(text, dest='en')
        print(f"[v0] Translated to English: {translated.text}")
        return translated.text
    except Exception as e:
        print(f"[v0] Translation error: {e}")
        return text

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database path
DB_PATH = 'data/grievance.db'

def get_db_connection():
    """Get a database connection with row factory"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db_if_needed():
    """Initialize database if it doesn't exist"""
    if not os.path.exists(DB_PATH):
        from init_db import init_database
        from seed_db import seed_database, migrate_existing_complaints
        init_database()
        seed_database()
        migrate_existing_complaints()

# Initialize database on startup
init_db_if_needed()

# Email configuration
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USER = os.getenv('EMAIL_USER', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
EMAIL_FROM = os.getenv('EMAIL_FROM', EMAIL_USER)

print("\n" + "="*50)
print("EMAIL CONFIGURATION")
print("="*50)
print(f"EMAIL_HOST: {EMAIL_HOST}")
print(f"EMAIL_PORT: {EMAIL_PORT}")
print(f"EMAIL_USER: {EMAIL_USER}")
print(f"EMAIL_PASSWORD: {'*' * len(EMAIL_PASSWORD) if EMAIL_PASSWORD else '(NOT SET)'}")
print(f"EMAIL_FROM: {EMAIL_FROM}")
if EMAIL_USER and EMAIL_PASSWORD:
    print("Email is CONFIGURED - emails will be sent")
else:
    print("Email is NOT CONFIGURED - OTPs will only print to console")
print("="*50 + "\n")

# Load ML models (fallback)
try:
    category_model = joblib.load('models/category_model.pkl')
    category_vectorizer = joblib.load('models/category_vectorizer.pkl')
    criticality_model = joblib.load('models/criticality_model.pkl')
    criticality_vectorizer = joblib.load('models/criticality_vectorizer.pkl')
    label_encoder = joblib.load('models/label_encoder.pkl')
    critical_keywords = joblib.load('models/critical_keywords.pkl')
    print("Models loaded successfully!")
except Exception as e:
    print(f"Error loading models: {e}")
    category_model = None
    category_vectorizer = None
    criticality_model = None
    criticality_vectorizer = None
    label_encoder = None
    critical_keywords = set()

# In-memory OTP storage for auth (temporary)
auth_otp_storage = {}

def generate_complaint_id():
    """Generate unique complaint ID"""
    return 'CMP' + ''.join(random.choices(string.digits, k=8))

def generate_otp():
    """Generate 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))

def generate_admin_id():
    """Generate unique admin ID"""
    return 'ADM' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def send_email(to_email, subject, body):
    """Send email using SMTP"""
    try:
        if not EMAIL_USER or not EMAIL_PASSWORD:
            print(f"[v0] Email not configured. Email would be sent to: {to_email}")
            print(f"[v0] Subject: {subject}")
            return False
        
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_FROM, to_email, text)
        server.quit()
        
        print(f"[v0] Email sent successfully to {to_email}")
        return True
    
    except Exception as e:
        print(f"[v0] Error sending email: {e}")
        return False

def send_status_update_email(complaint, new_status, admin_info=None):
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
    
    zone_name = complaint.get('zone_name', 'N/A')
    admin_id = admin_info.get('admin_id', 'N/A') if admin_info else 'N/A'
    department = complaint.get('category', 'N/A')
    
    body = f"""
Hello {complaint['name']},

{status_messages[new_status]['message']}

Complaint Details:
------------------
Complaint ID: {complaint['complaint_id']}
Department: {department}
Zone: {zone_name}
Admin ID: {admin_id}
Status: {new_status}
Locality: {complaint.get('locality_name', 'N/A')}

If you have any questions, please contact our support team.

Thank you,
Grievance Hub Team
Hyderabad Municipal Corporation
    """
    
    return send_email(
        complaint['email'],
        status_messages[new_status]['subject'],
        body
    )

# ====================
# API ROUTES
# ====================

@app.route('/', methods=['GET'])
def home():
    """API status endpoint"""
    return jsonify({
        'message': 'Grievance System API - Multi-Admin Version',
        'status': 'running',
        'database': 'SQLite',
        'version': '2.0',
        'endpoints': {
            'send_otp': '/api/auth/send-otp',
            'verify_otp': '/api/auth/verify-otp',
            'classify': '/api/classify',
            'submit': '/api/complaints/submit',
            'track': '/api/complaints/track',
            'admin_login': '/api/admin/login',
            'admin_complaints': '/api/admin/complaints',
            'update_status': '/api/admin/complaints/<id>/status',
            'categories': '/api/categories',
            'zones': '/api/zones',
            'areas': '/api/areas',
            'areas_by_zone': '/api/areas/<zone_id>'
        }
    })

# ====================
# ZONES & AREAS API
# ====================

@app.route('/api/zones', methods=['GET'])
def get_zones():
    """Get all zones"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT z.id, z.zone_number, z.zone_name,
                   COUNT(DISTINCT c.id) as circle_count,
                   COUNT(DISTINCT a.id) as area_count
            FROM zones z
            LEFT JOIN circles c ON c.zone_id = z.id
            LEFT JOIN areas a ON a.zone_id = z.id
            GROUP BY z.id
            ORDER BY z.zone_number
        ''')
        
        zones = []
        for row in cursor.fetchall():
            zones.append({
                'id': row['id'],
                'zone_number': row['zone_number'],
                'zone_name': row['zone_name'],
                'circle_count': row['circle_count'],
                'area_count': row['area_count']
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'zones': zones
        })
    
    except Exception as e:
        print(f"[v0] Error fetching zones: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/areas', methods=['GET'])
def get_all_areas():
    """Get all areas/localities with search support"""
    try:
        search = request.args.get('search', '').strip()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if search:
            cursor.execute('''
                SELECT a.id, a.area_name, a.ward_number, a.zone_id,
                       z.zone_name, z.zone_number, c.circle_name
                FROM areas a
                JOIN zones z ON z.id = a.zone_id
                JOIN circles c ON c.id = a.circle_id
                WHERE a.area_name LIKE ?
                ORDER BY a.area_name
                LIMIT 50
            ''', (f'%{search}%',))
        else:
            cursor.execute('''
                SELECT a.id, a.area_name, a.ward_number, a.zone_id,
                       z.zone_name, z.zone_number, c.circle_name
                FROM areas a
                JOIN zones z ON z.id = a.zone_id
                JOIN circles c ON c.id = a.circle_id
                ORDER BY z.zone_number, a.area_name
            ''')
        
        areas = []
        for row in cursor.fetchall():
            areas.append({
                'id': row['id'],
                'area_name': row['area_name'],
                'ward_number': row['ward_number'],
                'zone_id': row['zone_id'],
                'zone_name': row['zone_name'],
                'zone_number': row['zone_number'],
                'circle_name': row['circle_name'],
                'display_name': f"{row['area_name']} - Zone {row['zone_number']} ({row['zone_name']})"
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'areas': areas,
            'count': len(areas)
        })
    
    except Exception as e:
        print(f"[v0] Error fetching areas: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/areas/<int:zone_id>', methods=['GET'])
def get_areas_by_zone(zone_id):
    """Get areas for a specific zone"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.id, a.area_name, a.ward_number, c.circle_name, c.id as circle_id
            FROM areas a
            JOIN circles c ON c.id = a.circle_id
            WHERE a.zone_id = ?
            ORDER BY a.area_name
        ''', (zone_id,))
        
        areas = []
        for row in cursor.fetchall():
            areas.append({
                'id': row['id'],
                'area_name': row['area_name'],
                'ward_number': row['ward_number'],
                'circle_name': row['circle_name'],
                'circle_id': row['circle_id']
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'areas': areas
        })
    
    except Exception as e:
        print(f"[v0] Error fetching areas for zone: {e}")
        return jsonify({'error': str(e)}), 500

# ====================
# ADMIN AUTHENTICATION
# ====================

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """Admin login with role-based access"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
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
        
        if not admin:
            conn.close()
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Create session
        session_token = str(uuid.uuid4())
        expires_at = datetime.now() + timedelta(hours=24)
        
        cursor.execute('''
            INSERT INTO admin_sessions (session_token, admin_id, expires_at)
            VALUES (?, ?, ?)
        ''', (session_token, admin['id'], expires_at.isoformat()))
        
        conn.commit()
        conn.close()
        
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

# ====================
# AUTH OTP ENDPOINTS
# ====================

@app.route('/api/auth/send-otp', methods=['POST'])
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
        conn = get_db_connection()
        cursor = conn.cursor()
        
        expires_at = datetime.now() + timedelta(minutes=10)
        
        cursor.execute('''
            INSERT OR REPLACE INTO otp_storage (identifier, otp, otp_type, expires_at)
            VALUES (?, ?, 'auth', ?)
        ''', (email, otp, expires_at.isoformat()))
        
        conn.commit()
        conn.close()
        
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
        
        if not EMAIL_USER or not EMAIL_PASSWORD:
            response['otp'] = otp
            response['message'] = 'OTP generated (email not configured - check console)'
        
        return jsonify(response)
    
    except Exception as e:
        print(f"[v0] Error sending OTP: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/verify-otp', methods=['POST'])
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
            return jsonify({'error': 'OTP not found or expired'}), 404
        
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

# ====================
# COMPLAINT CLASSIFICATION
# ====================

@app.route('/api/classify', methods=['POST'])
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

        prompt = GEMINI_PROMPT.replace("<<<USER_COMPLAINT>>>", description)
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        text_response = response.text.strip()
        print("\nGemini raw response:\n", text_response)

        import re
        match = re.search(r'\{[\s\S]*\}', text_response)
        if match:
            result = json.loads(match.group())
            category = result.get("department", "General")
            criticality = result.get("criticality", "Non-Critical")
        else:
            category = "Invalid"
            criticality = "None"

        return jsonify({
            "category": category,
            "criticality": criticality,
            "success": True
        }), 200

    except Exception as e:
        print("Error in Gemini classification:", e)
        return jsonify({
            "category": "Invalid",
            "criticality": "None",
            "success": False
        }), 500

# ====================
# COMPLAINT SUBMISSION
# ====================

@app.route('/api/complaints/submit', methods=['POST'])
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
        try:
            prompt = GEMINI_PROMPT.replace("<<<USER_COMPLAINT>>>", description)
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            text_response = response.text.strip()

            import re
            match = re.search(r'\{[\s\S]*\}', text_response)
            if match:
                gemini_result = json.loads(match.group())
                category = gemini_result.get("department", "General")
                criticality = gemini_result.get("criticality", "Non-Critical")
            else:
                category = "General"
                criticality = "Non-Critical"

        except Exception as e:
            print(f"[v0] Gemini classification failed: {e}")
            category = "General"
            criticality = "Non-Critical"
        
        complaint_id = generate_complaint_id()
        
        # Save to database
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

# ====================
# COMPLAINT TRACKING
# ====================

@app.route('/api/complaints/track', methods=['POST'])
def track_complaint():
    """Track complaint with OTP verification"""
    try:
        data = request.json
        complaint_id = data.get('complaint_id')
        email = data.get('email')
        otp = data.get('otp')
        
        if not all([complaint_id, email, otp]):
            return jsonify({'error': 'Complaint ID, email, and OTP are required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verify OTP
        cursor.execute('''
            SELECT otp FROM otp_storage
            WHERE identifier = ? AND otp_type = 'tracking'
        ''', (f"{complaint_id}:{email}",))
        
        otp_record = cursor.fetchone()
        
        if not otp_record or otp_record['otp'] != otp:
            conn.close()
            return jsonify({'error': 'Invalid OTP'}), 401
        
        # Get complaint with zone info
        cursor.execute('''
            SELECT c.*, z.zone_name, z.zone_number, ci.circle_name
            FROM complaints c
            LEFT JOIN zones z ON z.id = c.zone_id
            LEFT JOIN circles ci ON ci.id = c.circle_id
            WHERE c.complaint_id = ? AND c.email = ?
        ''', (complaint_id, email))
        
        complaint = cursor.fetchone()
        
        if not complaint:
            conn.close()
            return jsonify({'error': 'Complaint not found'}), 404
        
        # Get status history
        cursor.execute('''
            SELECT * FROM complaint_status_history
            WHERE complaint_id = ?
            ORDER BY created_at DESC
        ''', (complaint['id'],))
        
        history = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
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

# ====================
# ADMIN COMPLAINTS MANAGEMENT
# ====================

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    categories = [
        "CM Office (Miscellaneous)",
        "Development Authority", 
        "Municipal",
        "Police",
        "Public Works Department",
        "Transport",
        "General"
    ]
    
    return jsonify({
        'success': True,
        'categories': categories
    })

@app.route('/api/admin/complaints', methods=['GET'])
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
        
        # Calculate statistics
        total = len(complaints)
        pending = len([c for c in complaints if c['status'] == 'Pending'])
        in_progress = len([c for c in complaints if c['status'] == 'In Progress'])
        resolved = len([c for c in complaints if c['status'] == 'Resolved'])
        critical = len([c for c in complaints if c.get('criticality') == 'Critical'])
        
        conn.close()
        
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

@app.route('/api/admin/complaints/<complaint_id>/status', methods=['PUT'])
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
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get current complaint
        cursor.execute('''
            SELECT c.*, z.zone_name FROM complaints c
            LEFT JOIN zones z ON z.id = c.zone_id
            WHERE c.complaint_id = ?
        ''', (complaint_id,))
        
        complaint = cursor.fetchone()
        
        if not complaint:
            conn.close()
            return jsonify({'error': 'Complaint not found'}), 404
        
        # Check if already resolved - cannot change
        if complaint['status'] == 'Resolved':
            conn.close()
            return jsonify({'error': 'Cannot modify resolved complaints'}), 403
        
        # Check admin's permission based on role
        if admin['role'] == 'department_admin':
            if complaint['circle_id'] != admin['circle_id']:
                conn.close()
                return jsonify({'error': 'Not authorized to modify this complaint'}), 403
        elif admin['role'] == 'sub_admin':
            if complaint['zone_id'] != admin['zone_id']:
                conn.close()
                return jsonify({'error': 'Not authorized to modify this complaint'}), 403
        
        old_status = complaint['status']
        resolved_at = datetime.now().isoformat() if new_status == 'Resolved' else None
        
        # Update complaint
        cursor.execute('''
            UPDATE complaints
            SET status = ?, updated_at = ?, resolved_at = ?, assigned_admin_id = ?
            WHERE complaint_id = ?
        ''', (new_status, datetime.now().isoformat(), resolved_at, admin['id'], complaint_id))
        
        # Log status change
        cursor.execute('''
            INSERT INTO complaint_status_history 
            (complaint_id, old_status, new_status, changed_by_admin_id, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (complaint['id'], old_status, new_status, admin['id'], notes))
        
        conn.commit()
        conn.close()
        
        # Send email notification
        complaint_dict = dict(complaint)
        complaint_dict['zone_name'] = complaint['zone_name']
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

@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    """Admin logout - invalidate session"""
    try:
        session_token = request.headers.get('X-Session-Token')
        
        if session_token:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE admin_sessions SET is_active = 0 WHERE session_token = ?
            ''', (session_token,))
            
            conn.commit()
            conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        })
    
    except Exception as e:
        print(f"[v0] Error in logout: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/profile', methods=['GET'])
def get_admin_profile():
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

if __name__ == '__main__':
    os.makedirs('models', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    app.run(debug=True, port=5000)

