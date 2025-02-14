from collections import defaultdict
from typing import List, Dict, Tuple
from datetime import date
from app.models.project import Project
from app.models.etp_entry import EtpEntry
from app.constants import TimeConstants
from datetime import datetime
from app import db

class EtpService:
    @staticmethod
    def get_stored_etp(project_name: str, period: str) -> float:
        """Récupère la valeur ETP stockée pour un projet et une période donnés"""
        entry = EtpEntry.query.filter_by(
            project_name=project_name,
            period=period
        ).first()
        return entry.etp_value if entry else None

    @staticmethod
    def get_period_for_date(target_date: date) -> str:
        """Détermine la période correspondant à une date donnée"""
        if target_date.year == 2025:
            if target_date.month <= 6:
                return "2025 Q1-Q2"
            else:
                return "2025 Q3-Q4"
        else:
            return "2026-2027"

    @staticmethod
    def get_task_etp_by_date(project_name: str, task_date: date, default_etp: float) -> float:
        """Récupère l'ETP pour une tâche à une date spécifique"""
        period = EtpService.get_period_for_date(task_date)
        stored_etp = EtpService.get_stored_etp(project_name, period)
        return stored_etp if stored_etp is not None else default_etp

    @staticmethod
    def calculate_etp_per_period(projects: List[Project]) -> Tuple[List[Dict], Dict[str, float]]:
        etp_data = []
        period_totals = defaultdict(float)
        
        for project in projects:
            project_etps = defaultdict(float)
            max_etp = 0
            
            stored_etps = EtpEntry.query.filter_by(project_name=project.name).all()
            stored_etps_dict = {entry.period: entry.etp_value for entry in stored_etps}
            
            for task in project.tasks:
                period_start = EtpService.get_period_for_date(task.start_date)
                period_end = EtpService.get_period_for_date(task.end_date)
                max_etp = max(max_etp, task.etp)
                
                # Assigner l'ETP à toutes les périodes concernées
                for period in [period_start, period_end]:
                    stored_value = stored_etps_dict.get(period)
                    if stored_value is not None:
                        project_etps[period] = stored_value
                    else:
                        project_etps[period] = max(project_etps[period], task.etp)
                
                # Si la tâche s'étend sur 2025 Q3-Q4 et commence en Q1-Q2 ou finit en 2026-2027
                if period_start != period_end and period_start == "2025 Q1-Q2":
                    middle_period = "2025 Q3-Q4"
                    stored_value = stored_etps_dict.get(middle_period)
                    if stored_value is not None:
                        project_etps[middle_period] = stored_value
                    else:
                        project_etps[middle_period] = max(project_etps[middle_period], task.etp)
            
            project_row = {
                "name": project.name,
                **{period: project_etps[period] for period in TimeConstants.PERIODS_MAPPING.values()},
                "total": max_etp
            }
            
            for period_name, value in project_etps.items():
                period_totals[period_name] += value
            
            etp_data.append(project_row)
        
        return etp_data, period_totals

    @staticmethod
    def update_etp(project_name: str, period: str, etp_value: float) -> None:
        """Update ETP value in database"""
        entry = EtpEntry.query.filter_by(
            project_name=project_name,
            period=period
        ).first()
        
        if entry:
            entry.etp_value = etp_value
            entry.updated_at = datetime.utcnow()
        else:
            entry = EtpEntry(
                project_name=project_name,
                period=period,
                etp_value=etp_value
            )
            db.session.add(entry)
            
        db.session.commit()