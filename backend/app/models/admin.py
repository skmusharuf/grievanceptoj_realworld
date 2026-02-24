from app.extensions import db
from datetime import datetime


class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), nullable=False)  # super_admin, sub_admin, department_admin
    department = db.Column(db.String(100))
    zone_id = db.Column(db.Integer, db.ForeignKey('zones.id'))
    circle_id = db.Column(db.Integer, db.ForeignKey('circles.id'))
    is_active = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sessions = db.relationship('AdminSession', backref='admin', lazy=True)
    assigned_complaints = db.relationship('Complaint', backref='assigned_admin', lazy=True, foreign_keys='Complaint.assigned_admin_id')
    status_changes = db.relationship('ComplaintStatusHistory', backref='changed_by_admin', lazy=True)
