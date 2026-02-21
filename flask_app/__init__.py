"""
Grievance Hub Flask Application Factory
"""

from flask import Flask
from flask_cors import CORS
from .config import Config


def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )
    app.config.from_object(config_class)

    # Enable CORS
    CORS(app)

    # Initialize database
    from .database import init_db_if_needed
    with app.app_context():
        init_db_if_needed(app.config['DB_PATH'])

    # Load ML models
    from .services.classifier import ClassifierService
    ClassifierService.load_models(app.config['MODELS_DIR'])

    # Register blueprints
    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .routes.complaints import complaints_bp
    from .routes.admin import admin_bp
    from .routes.zones import zones_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(complaints_bp, url_prefix='/api/complaints')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(zones_bp, url_prefix='/api')

    return app
