from app import db
from datetime import datetime

class EtpEntry(db.Model):
    __tablename__ = 'etp_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    period = db.Column(db.String(20), nullable=False)
    etp_value = db.Column(db.Float, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('project_name', 'period', name='uix_project_period'),
    )
