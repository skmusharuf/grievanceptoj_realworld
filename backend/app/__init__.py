from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.extensions import db


def create_app():
    app = Flask(
        __name__,
        static_folder='static',
        template_folder='templates'
    )
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    CORS(app)

    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.complaint_routes import complaint_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.zone_routes import zone_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(complaint_bp, url_prefix='/api/complaints')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(zone_bp, url_prefix='/api')

    # Home route
    @app.route('/', methods=['GET'])
    def home():
        from flask import jsonify
        return jsonify({
            'message': 'Grievance System API - Multi-Admin Version',
            'status': 'running',
            'database': 'SQLite (Flask-SQLAlchemy ORM)',
            'version': '2.0',
            'endpoints': {
                'send_otp': '/api/auth/send-otp',
                'verify_otp': '/api/auth/verify-otp',
                'classify': '/api/complaints/classify',
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

    @app.route('/api/categories', methods=['GET'])
    def get_categories():
        from flask import jsonify
        categories = [
            "CM Office (Miscellaneous)",
            "Development Authority",
            "Municipal",
            "Police",
            "Public Works Department",
            "Transport",
            "General"
        ]
        return jsonify({'success': True, 'categories': categories})

    return app
