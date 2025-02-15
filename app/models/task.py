from app import db
from datetime import datetime, date

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    comment = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    color = db.Column(db.String(50), nullable=False)
    etp = db.Column(db.Float, default=1.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def _calculate_grid_position(self):
        """Calcule la position relative dans la grille."""
        def get_quarter_position(d: date) -> float:
            if d.year > 2025:
                return 80.0
            
            quarter = (d.month - 1) // 3
            base_position = quarter * 20.0
            
            month_in_quarter = (d.month - 1) % 3
            days_in_quarter = 90
            days_from_quarter_start = (month_in_quarter * 30) + (d.day - 1)
            relative_position = (days_from_quarter_start / days_in_quarter) * 20.0
            
            return base_position + relative_position
        
        start_pos = get_quarter_position(self.start_date)
        end_pos = get_quarter_position(self.end_date)
        
        if end_pos < start_pos:
            end_pos = 100.0
        
        width = end_pos - start_pos
        
        if width < 15 and (self.end_date.month - self.start_date.month >= 1):
            width = 15
        elif width < 8:
            width = 8
        
        return start_pos, width
    
    def to_dict(self):
        start, width = self._calculate_grid_position()
        return {
            'id': self.id,
            'project_id': self.project_id,
            'text': self.text,
            'comment': self.comment or '',
            'start_date': self.start_date.strftime('%d/%m/%Y'),  # Format de date pour l'affichage
            'end_date': self.end_date.strftime('%d/%m/%Y'),      # Format de date pour l'affichage
            'dates': f"{self.start_date.strftime('%d/%m/%Y')} - {self.end_date.strftime('%d/%m/%Y')}", # Pour l'infobulle
            'raw_start_date': self.start_date.isoformat(),  # Pour l'édition
            'raw_end_date': self.end_date.isoformat(),      # Pour l'édition
            'color': self.color,
            'etp': self.etp,
            'start': start,
            'width': width
        }
