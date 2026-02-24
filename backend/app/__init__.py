from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()

def create_app(config_name='development'):
    """Application factory function"""
    app = Flask(__name__)
    
    # Configuration
    if config_name == 'production':
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///grievance.db')
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///../data/grievance.db')
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes import auth_routes, complaint_routes, admin_routes, zone_routes
    
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(complaint_routes.bp)
    app.register_blueprint(admin_routes.bp)
    app.register_blueprint(zone_routes.bp)
    
    # Health check endpoint
    @app.route('/', methods=['GET'])
    def home():
        return {
            'message': 'Grievance System API - Multi-Admin Version',
            'status': 'running',
            'database': 'SQLite with SQLAlchemy',
            'version': '2.0'
        }, 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
