"""Helper functions"""

import random
import string

def generate_complaint_id():
    """Generate unique complaint ID"""
    return 'CMP' + ''.join(random.choices(string.digits, k=8))

def generate_otp():
    """Generate 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))

def generate_admin_id():
    """Generate unique admin ID"""
    return 'ADM' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
