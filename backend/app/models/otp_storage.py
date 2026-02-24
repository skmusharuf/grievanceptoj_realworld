from app.extensions import db
from datetime import datetime


class OTPStorage(db.Model):
    __tablename__ = 'otp_storage'

    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(300), unique=True, nullable=False, index=True)
    otp = db.Column(db.String(10), nullable=False)
    otp_type = db.Column(db.String(20), default='auth')  # auth, tracking
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    is_used = db.Column(db.Integer, default=0)
