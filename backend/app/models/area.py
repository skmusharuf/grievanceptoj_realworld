from app.extensions import db
from datetime import datetime


class Area(db.Model):
    __tablename__ = 'areas'

    id = db.Column(db.Integer, primary_key=True)
    area_name = db.Column(db.String(200), nullable=False, index=True)
    ward_number = db.Column(db.Integer)
    circle_id = db.Column(db.Integer, db.ForeignKey('circles.id'), nullable=False)
    zone_id = db.Column(db.Integer, db.ForeignKey('zones.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    complaints = db.relationship('Complaint', backref='area', lazy=True)
