"""Main Flask application entry point"""

import os
import joblib
from flask import jsonify
from app import create_app
from app.config import log_email_config, DB_PATH
from app.models.database import init_db_if_needed

# Create Flask app
app = create_app()

# Initialize database on startup
init_db_if_needed()

# Log email configuration
log_email_config()

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

# ====================
# HOME ROUTE
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

if __name__ == '__main__':
    os.makedirs('models', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    app.run(debug=True, port=5000)
