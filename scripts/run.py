"""
Run the Grievance System Flask Application
This is the main entry point for the application
"""

from app.main import app

if __name__ == '__main__':
    app.run(debug=True, port=5000)
