"""
Grievance System - Flask Application with HTML Templates
Simple, easy to understand architecture
"""

from flask import Flask
from flask_cors import CORS
import os

def create_app():
    """Create and configure the Flask app"""
    # Setup paths
    app_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(app_dir, 'templates')
    static_dir = os.path.join(app_dir, 'static')
    
    # Create Flask app with custom paths
    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir,
        static_url_path='/static'
    )
    
    CORS(app)
    
    # Register blueprints
    from .routes import auth, zones, complaints, admin, categories
    from .routes.pages import pages_bp
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(zones.bp)
    app.register_blueprint(complaints.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(categories.bp)
    app.register_blueprint(pages_bp)
    
    return app
