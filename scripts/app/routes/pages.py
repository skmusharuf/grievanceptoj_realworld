"""Pages Blueprint - Serves HTML pages"""
from flask import Blueprint, render_template, session, redirect, url_for

pages_bp = Blueprint('pages', __name__)

@pages_bp.route('/')
def home():
    """Home page"""
    return render_template('index.html')

@pages_bp.route('/submit-complaint')
def submit_complaint():
    """Submit complaint page"""
    return render_template('submit-complaint.html')

@pages_bp.route('/track')
def track_complaint():
    """Track complaint page"""
    return render_template('track.html')

@pages_bp.route('/admin/login')
def admin_login():
    """Admin login page"""
    return render_template('admin-login.html')

@pages_bp.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard page"""
    session_token = session.get('admin_session_token')
    if not session_token:
        return redirect(url_for('pages.admin_login'))
    return render_template('admin-dashboard.html')
