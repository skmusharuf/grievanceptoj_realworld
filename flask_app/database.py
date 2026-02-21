"""
Database connection and initialization utilities
"""

import sqlite3
import os


def get_db_connection(db_path):
    """Get a database connection with row factory"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db_if_needed(db_path):
    """Initialize database if it doesn't exist"""
    if not os.path.exists(db_path):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        _create_tables(db_path)
        print(f"[GrievanceHub] Database created at: {db_path}")
    else:
        print(f"[GrievanceHub] Database found at: {db_path}")


def _create_tables(db_path):
    """Create all required database tables"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS zones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            zone_number INTEGER UNIQUE NOT NULL,
            zone_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

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
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_areas_name ON areas(area_name)')

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
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_complaints_zone ON complaints(zone_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_complaints_status ON complaints(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_complaints_admin ON complaints(assigned_admin_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_complaints_category ON complaints(category)')

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
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_otp_identifier ON otp_storage(identifier)')

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

    conn.commit()
    conn.close()
