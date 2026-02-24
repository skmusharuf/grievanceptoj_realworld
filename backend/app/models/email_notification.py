from app.extensions import db
from datetime import datetime


class EmailNotification(db.Model):
    __tablename__ = 'email_notifications'

    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.id'))
    recipient_email = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(500), nullable=False)
    body = db.Column(db.Text)
    notification_type = db.Column(db.String(50))
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_sent = db.Column(db.Integer, default=0)
