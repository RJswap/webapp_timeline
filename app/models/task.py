from dataclasses import dataclass
import re
from typing import Optional
from datetime import date, datetime

@dataclass
class Task:
    start_date: date
    end_date: date
    color: str
    text: str
    etp: Optional[float] = None
    
    def __post_init__(self):
        if self.etp is None:
            self.etp = self._extract_etp_from_text()
    
    def _extract_etp_from_text(self) -> float:
        etp_pattern = r'\((\d*\.?\d+)\s*ETP\)'
        match = re.search(etp_pattern, self.text)
        return float(match.group(1)) if match else 0.0
    
    def _calculate_grid_position(self) -> tuple[float, float]:
        """Calcule la position relative dans la grille.
        La grille est divisée en 5 colonnes égales de 20% chacune:
        - 2025 Q1: 0-20%
        - 2025 Q2: 20-40%
        - 2025 Q3: 40-60%
        - 2025 Q4: 60-80%
        - 2026-2027: 80-100%
        """
        def get_quarter_position(d: date) -> float:
            if d.year > 2025:
                return 80.0
            
            quarter = (d.month - 1) // 3  # 0-3 pour Q1-Q4
            base_position = quarter * 20.0  # Position de début du trimestre
            
            # Position relative dans le trimestre (0-20%)
            month_in_quarter = (d.month - 1) % 3
            days_in_quarter = 90  # Approximation pour un calcul plus simple
            days_from_quarter_start = (month_in_quarter * 30) + (d.day - 1)
            relative_position = (days_from_quarter_start / days_in_quarter) * 20.0
            
            return base_position + relative_position
        
        start_pos = get_quarter_position(self.start_date)
        end_pos = get_quarter_position(self.end_date)
        
        # Ajuster la largeur pour les tâches qui traversent les trimestres
        if end_pos < start_pos:  # Si la tâche se termine en 2026-2027
            end_pos = 100.0
        
        # Calculer la largeur
        width = end_pos - start_pos
        
        # Ajuster la largeur minimale pour la visibilité
        if width < 15 and (self.end_date.month - self.start_date.month >= 1):
            width = 15  # Largeur minimum pour les tâches de 2 mois ou plus
        elif width < 8:
            width = 8  # Largeur minimum pour les tâches courtes
        
        # Pour débogage
        print(f"Task: {self.text}")
        print(f"Dates: {self.start_date} -> {self.end_date}")
        print(f"Position: {start_pos:.1f}% -> {end_pos:.1f}%")
        print(f"Width: {width:.1f}%")
        print("---")
        
        return start_pos, width
    
    def to_dict(self):
        start, width = self._calculate_grid_position()
        return {
            'start': start,
            'width': width,
            'color': self.color,
            'text': self.text,
            'etp': self.etp,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat()
        }