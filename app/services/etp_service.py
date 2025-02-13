from collections import defaultdict
from typing import List, Dict, Tuple
from datetime import datetime
from app.models.project import Project
from app.models.etp_entry import EtpEntry
from app.constants import TimeConstants
from app import db

class EtpService:
    @staticmethod
    def calculate_etp_per_period(projects: List[Project]) -> Tuple[List[Dict], Dict[str, float]]:
        etp_data = []
        period_totals = defaultdict(float)
        
        for project in projects:
            project_etps = defaultdict(float)
            max_etp = 0
            
            # Get stored ETP values from database
            stored_etps = EtpEntry.query.filter_by(project_name=project.name).all()
            stored_etps_dict = {entry.period: entry.etp_value for entry in stored_etps}
            
            for task in project.tasks:
                start_period = (task.start + 1) // 2
                width_periods = (task.width + 1) // 2
                max_etp = max(max_etp, task.etp)
                
                for period in range(start_period, start_period + width_periods):
                    period_name = TimeConstants.PERIODS_MAPPING.get(period)
                    if period_name:
                        # Use stored value if available, otherwise use calculated value
                        stored_value = stored_etps_dict.get(period_name)
                        if stored_value is not None:
                            project_etps[period_name] = stored_value
                        else:
                            project_etps[period_name] = max(project_etps[period_name], task.etp)
            
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
        try:
            if not project_name or not period:
                raise ValueError("Project name and period are required")
                
            if not isinstance(etp_value, (int, float)) or etp_value < 0:
                raise ValueError("ETP value must be a non-negative number")

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
                    etp_value=etp_value,
                    updated_at=datetime.utcnow()
                )
                db.session.add(entry)
                
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to update ETP: {str(e)}")