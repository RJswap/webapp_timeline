from app import db
from datetime import datetime

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    color_scheme = db.Column(db.String(50), nullable=False, default='blue')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    tasks = db.relationship('Task', backref='project', lazy=True, cascade='all, delete-orphan')
    etp_entries = db.relationship('EtpEntry', backref='project', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'color_scheme': self.color_scheme,
            'tasks': [task.to_dict() for task in self.tasks]
        }