from app import db
from datetime import datetime, timedelta
import uuid
import random
import string
import hashlib

class Zone(db.Model):
    """Zone model - Admin divisions"""
    __tablename__ = 'zones'
    
    id = db.Column(db.Integer, primary_key=True)
    zone_number = db.Column(db.Integer, unique=True, nullable=False)
    zone_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    circles = db.relationship('Circle', backref='zone', lazy=True, cascade='all, delete-orphan')
    areas = db.relationship('Area', backref='zone', lazy=True, cascade='all, delete-orphan')
    admins = db.relationship('Admin', backref='zone', lazy=True)
    complaints = db.relationship('Complaint', backref='zone', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'zone_number': self.zone_number,
            'zone_name': self.zone_name,
            'circle_count': len(self.circles),
            'area_count': len(self.areas)
        }


class Circle(db.Model):
    """Circle model - Sub-divisions of zones"""
    __tablename__ = 'circles'
    
    id = db.Column(db.Integer, primary_key=True)
    circle_number = db.Column(db.Integer, nullable=False)
    circle_name = db.Column(db.String(255), nullable=False)
    zone_id = db.Column(db.Integer, db.ForeignKey('zones.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    areas = db.relationship('Area', backref='circle', lazy=True, cascade='all, delete-orphan')
    admins = db.relationship('Admin', backref='circle', lazy=True)
    complaints = db.relationship('Complaint', backref='circle', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'circle_number': self.circle_number,
            'circle_name': self.circle_name,
            'zone_id': self.zone_id
        }


class Area(db.Model):
    """Area/Locality model"""
    __tablename__ = 'areas'
    
    id = db.Column(db.Integer, primary_key=True)
    area_name = db.Column(db.String(255), nullable=False)
    ward_number = db.Column(db.Integer)
    circle_id = db.Column(db.Integer, db.ForeignKey('circles.id'), nullable=False)
    zone_id = db.Column(db.Integer, db.ForeignKey('zones.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    complaints = db.relationship('Complaint', backref='area', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'area_name': self.area_name,
            'ward_number': self.ward_number,
            'zone_id': self.zone_id,
            'circle_id': self.circle_id,
            'zone_name': self.zone.zone_name,
            'zone_number': self.zone.zone_number,
            'circle_name': self.circle.circle_name,
            'display_name': f"{self.area_name} - Zone {self.zone.zone_number} ({self.zone.zone_name})"
        }


class Admin(db.Model):
    """Admin user model with role-based access"""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(50), nullable=False)  # super_admin, sub_admin, department_admin
    department = db.Column(db.String(255))
    zone_id = db.Column(db.Integer, db.ForeignKey('zones.id'))
    circle_id = db.Column(db.Integer, db.ForeignKey('circles.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sessions = db.relationship('AdminSession', backref='admin', lazy=True, cascade='all, delete-orphan')
    complaints = db.relationship('Complaint', backref='assigned_admin', lazy=True)
    status_changes = db.relationship('ComplaintStatusHistory', backref='admin', lazy=True)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        """Verify password"""
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()
    
    def to_dict(self):
        return {
            'id': self.id,
            'admin_id': self.admin_id,
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'department': self.department,
            'zone_id': self.zone_id,
            'zone_name': self.zone.zone_name if self.zone else None,
            'circle_id': self.circle_id,
            'circle_name': self.circle.circle_name if self.circle else None
        }


class Complaint(db.Model):
    """Complaint/Grievance model"""
    __tablename__ = 'complaints'
    
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    aadhar = db.Column(db.String(20))
    description = db.Column(db.Text, nullable=False)
    full_address = db.Column(db.Text)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'))
    zone_id = db.Column(db.Integer, db.ForeignKey('zones.id'))
    circle_id = db.Column(db.Integer, db.ForeignKey('circles.id'))
    locality_name = db.Column(db.String(255))
    category = db.Column(db.String(255))  # Department classification
    criticality = db.Column(db.String(50), default='Non-Critical')
    status = db.Column(db.String(50), default='Pending')  # Pending, In Progress, Resolved
    assigned_admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'))
    resolution_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    
    # Relationships
    status_history = db.relationship('ComplaintStatusHistory', backref='complaint', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.complaint_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'aadhar': self.aadhar,
            'description': self.description,
            'full_address': self.full_address,
            'locality_name': self.locality_name,
            'zone_name': self.zone.zone_name if self.zone else None,
            'zone_number': self.zone.zone_number if self.zone else None,
            'circle_name': self.circle.circle_name if self.circle else None,
            'category': self.category,
            'criticality': self.criticality,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None
        }


class ComplaintStatusHistory(db.Model):
    """Status change history for complaints"""
    __tablename__ = 'complaint_status_history'
    
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.id'), nullable=False)
    old_status = db.Column(db.String(50))
    new_status = db.Column(db.String(50), nullable=False)
    changed_by_admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'old_status': self.old_status,
            'new_status': self.new_status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }


class OTPStorage(db.Model):
    """OTP storage for authentication and tracking"""
    __tablename__ = 'otp_storage'
    
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(255), unique=True, nullable=False)
    otp = db.Column(db.String(10), nullable=False)
    otp_type = db.Column(db.String(50), default='auth')  # auth, tracking
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    is_used = db.Column(db.Boolean, default=False)


class AdminSession(db.Model):
    """Admin session management"""
    __tablename__ = 'admin_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_token = db.Column(db.String(255), unique=True, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)


class EmailNotification(db.Model):
    """Email notification log"""
    __tablename__ = 'email_notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.id'))
    recipient_email = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text)
    notification_type = db.Column(db.String(100))
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_sent = db.Column(db.Boolean, default=False)
