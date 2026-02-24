"""
Main entry point for the Grievance System Flask application.
Run this file to start the development server.
"""
import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    os.makedirs('instance', exist_ok=True)
    app.run(debug=True, port=5000)
