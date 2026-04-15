"""Database connection and utilities"""

import sqlite3
import os
from app.config import DB_PATH

def get_db_connection():
    """Get a database connection with row factory"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db_if_needed():
    """Initialize database if it doesn't exist"""
    if not os.path.exists(DB_PATH):
        from init_db import init_database
        from seed_db import seed_database, migrate_existing_complaints
        init_database()
        seed_database()
        migrate_existing_complaints()
