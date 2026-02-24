from app.extensions import db
from datetime import datetime


class Complaint(db.Model):
    __tablename__ = 'complaints'

    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))
    aadhar = db.Column(db.String(20))
    description = db.Column(db.Text, nullable=False)
    full_address = db.Column(db.Text)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'))
    zone_id = db.Column(db.Integer, db.ForeignKey('zones.id'), index=True)
    circle_id = db.Column(db.Integer, db.ForeignKey('circles.id'))
    locality_name = db.Column(db.String(200))
    category = db.Column(db.String(100), index=True)
    criticality = db.Column(db.String(20), default='Non-Critical')
    status = db.Column(db.String(20), default='Pending', index=True)  # Pending, In Progress, Resolved
    assigned_admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), index=True)
    resolution_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)

    status_history = db.relationship('ComplaintStatusHistory', backref='complaint', lazy=True)
    email_notifications = db.relationship('EmailNotification', backref='complaint', lazy=True)
