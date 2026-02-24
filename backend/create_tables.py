"""
Database initialization script.
Creates all tables defined in the SQLAlchemy models.
Run this before starting the application for the first time.
"""
import os
from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    os.makedirs('instance', exist_ok=True)
    db.create_all()
    print("All database tables created successfully!")
    print(f"Database location: {app.config['SQLALCHEMY_DATABASE_URI']}")
