from dataclasses import dataclass
import re
from typing import Optional

@dataclass
class Task:
    start: int
    width: int
    color: str
    text: str
    etp: Optional[float] = None
    
    def __post_init__(self):
        if self.etp is None:
            self.etp = self._extract_etp_from_text()
    
    def _extract_etp_from_text(self) -> float:
        """Extrait la valeur ETP du texte de manière plus robuste."""
        # Pattern pour trouver les valeurs ETP comme (1 ETP) ou (0.5 ETP) ou (1.5 ETP)
        etp_pattern = r'\((\d*\.?\d+)\s*ETP\)'
        match = re.search(etp_pattern, self.text)
        
        if match:
            try:
                return float(match.group(1))
            except (ValueError, IndexError):
                return 0.0
        return 0.0
    
    def to_dict(self):
        return {
            'start': self.start,
            'width': self.width,
            'color': self.color,
            'text': self.text,
            'etp': self.etp
        }