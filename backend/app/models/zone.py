from app.extensions import db
from datetime import datetime


class Zone(db.Model):
    __tablename__ = 'zones'

    id = db.Column(db.Integer, primary_key=True)
    zone_number = db.Column(db.Integer, unique=True, nullable=False)
    zone_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    circles = db.relationship('Circle', backref='zone', lazy=True)
    areas = db.relationship('Area', backref='zone', lazy=True)
    admins = db.relationship('Admin', backref='zone', lazy=True)
    complaints = db.relationship('Complaint', backref='zone', lazy=True)
