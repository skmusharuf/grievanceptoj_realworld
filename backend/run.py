#!/usr/bin/env python
"""
Main entry point for the Flask application
Run with: python run.py
"""

from app import create_app, db
from app.models import Zone, Circle, Area, Admin
import os

app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Register models for flask shell"""
    return {
        'db': db,
        'Zone': Zone,
        'Circle': Circle,
        'Area': Area,
        'Admin': Admin
    }

if __name__ == '__main__':
    with app.app_context():
        # Initialize database
        db.create_all()
        
        # Initialize seed data if needed
        from scripts.seed_db import seed_database
        seed_database()
    
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        use_reloader=debug
    )
