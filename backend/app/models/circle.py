from app.extensions import db
from datetime import datetime


class Circle(db.Model):
    __tablename__ = 'circles'

    id = db.Column(db.Integer, primary_key=True)
    circle_number = db.Column(db.Integer, nullable=False)
    circle_name = db.Column(db.String(100), nullable=False)
    zone_id = db.Column(db.Integer, db.ForeignKey('zones.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    areas = db.relationship('Area', backref='circle', lazy=True)
    admins = db.relationship('Admin', backref='circle', lazy=True)
    complaints = db.relationship('Complaint', backref='circle', lazy=True)
