"""
Grievance System - Modular Flask Application
Organized into separate modules for better maintainability
"""

from flask import Flask
from flask_cors import CORS

def create_app():
    """Create and configure the Flask app"""
    app = Flask(__name__)
    CORS(app)
    
    # Register blueprints
    from app.routes import auth, zones, complaints, admin, categories
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(zones.bp)
    app.register_blueprint(complaints.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(categories.bp)
    
    return app
