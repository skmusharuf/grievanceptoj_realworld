"""
Database Initialization Script for Grievance System
Creates SQLite database with all required tables for multi-admin hierarchy
"""

import sqlite3
import os

DB_PATH = 'data/grievance.db'

def init_database():
    """Initialize the SQLite database with all required tables"""
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Connect to database (creates if doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # ====================
    # ZONES TABLE
    # ====================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS zones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            zone_number INTEGER UNIQUE NOT NULL,
            zone_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # ====================
    # CIRCLES TABLE (Sub-divisions of zones)
    # ====================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS circles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            circle_number INTEGER NOT NULL,
            circle_name TEXT NOT NULL,
            zone_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (zone_id) REFERENCES zones(id)
        )
    ''')
    
    # ====================
    # AREAS/LOCALITIES TABLE
    # ====================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS areas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_name TEXT NOT NULL,
            ward_number INTEGER,
            circle_id INTEGER NOT NULL,
            zone_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (circle_id) REFERENCES circles(id),
            FOREIGN KEY (zone_id) REFERENCES zones(id)
        )
    ''')
    
    # Create index for fast area search
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_areas_name ON areas(area_name)
    ''')
    
    # ====================
    # ADMINS TABLE
    # ====================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            phone TEXT,
            role TEXT NOT NULL CHECK(role IN ('super_admin', 'sub_admin', 'department_admin')),
            department TEXT,
            zone_id INTEGER,
            circle_id INTEGER,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (zone_id) REFERENCES zones(id),
            FOREIGN KEY (circle_id) REFERENCES circles(id)
        )
    ''')
    
    # ====================
    # COMPLAINTS TABLE
    # ====================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            aadhar TEXT,
            description TEXT NOT NULL,
            full_address TEXT,
            area_id INTEGER,
            zone_id INTEGER,
            circle_id INTEGER,
            locality_name TEXT,
            category TEXT,
            criticality TEXT DEFAULT 'Non-Critical',
            status TEXT DEFAULT 'Pending' CHECK(status IN ('Pending', 'In Progress', 'Resolved')),
            assigned_admin_id INTEGER,
            resolution_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved_at TIMESTAMP,
            FOREIGN KEY (area_id) REFERENCES areas(id),
            FOREIGN KEY (zone_id) REFERENCES zones(id),
            FOREIGN KEY (circle_id) REFERENCES circles(id),
            FOREIGN KEY (assigned_admin_id) REFERENCES admins(id)
        )
    ''')
    
    # Create indexes for fast querying
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_complaints_zone ON complaints(zone_id)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_complaints_status ON complaints(status)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_complaints_admin ON complaints(assigned_admin_id)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_complaints_category ON complaints(category)
    ''')
    
    # ====================
    # COMPLAINT STATUS HISTORY TABLE
    # ====================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaint_status_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id INTEGER NOT NULL,
            old_status TEXT,
            new_status TEXT NOT NULL,
            changed_by_admin_id INTEGER,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (complaint_id) REFERENCES complaints(id),
            FOREIGN KEY (changed_by_admin_id) REFERENCES admins(id)
        )
    ''')
    
    # ====================
    # OTP STORAGE TABLE
    # ====================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS otp_storage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            identifier TEXT UNIQUE NOT NULL,
            otp TEXT NOT NULL,
            otp_type TEXT DEFAULT 'auth' CHECK(otp_type IN ('auth', 'tracking')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            is_used INTEGER DEFAULT 0
        )
    ''')
    
    # Create index for OTP lookup
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_otp_identifier ON otp_storage(identifier)
    ''')
    
    # ====================
    # ADMIN SESSIONS TABLE
    # ====================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_token TEXT UNIQUE NOT NULL,
            admin_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            is_active INTEGER DEFAULT 1,
            FOREIGN KEY (admin_id) REFERENCES admins(id)
        )
    ''')
    
    # ====================
    # EMAIL NOTIFICATIONS LOG TABLE
    # ====================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS email_notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id INTEGER,
            recipient_email TEXT NOT NULL,
            subject TEXT NOT NULL,
            body TEXT,
            notification_type TEXT,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_sent INTEGER DEFAULT 0,
            FOREIGN KEY (complaint_id) REFERENCES complaints(id)
        )
    ''')
    
    # Commit changes
    conn.commit()
    
    print("=" * 50)
    print("DATABASE INITIALIZATION COMPLETE")
    print("=" * 50)
    print(f"Database created at: {DB_PATH}")
    print("\nTables created:")
    print("  - zones (12 zones for Hyderabad)")
    print("  - circles (60 circles)")
    print("  - areas (300 wards/localities)")
    print("  - admins (super_admin, sub_admin, department_admin)")
    print("  - complaints")
    print("  - complaint_status_history")
    print("  - otp_storage")
    print("  - admin_sessions")
    print("  - email_notifications")
    print("=" * 50)
    
    conn.close()
    return True

def check_database():
    """Check if database exists and has all tables"""
    if not os.path.exists(DB_PATH):
        return False
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    required_tables = [
        'zones', 'circles', 'areas', 'admins', 'complaints',
        'complaint_status_history', 'otp_storage', 'admin_sessions',
        'email_notifications'
    ]
    
    conn.close()
    
    return all(table in tables for table in required_tables)

if __name__ == '__main__':
    init_database()
