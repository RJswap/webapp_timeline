from collections import defaultdict
from typing import List, Dict, Tuple
from app.models.project import Project
from app.constants import TimeConstants

class EtpService:
    @staticmethod
    def calculate_etp_per_period(projects: List[Project]) -> Tuple[List[Dict], Dict[str, float]]:
        etp_data = []
        period_totals = defaultdict(float)
        
        for project in projects:
            project_etps = defaultdict(float)
            max_etp = 0
            
            for task in project.tasks:
                start_period = (task.start + 1) // 2
                width_periods = (task.width + 1) // 2
                max_etp = max(max_etp, task.etp)
                
                for period in range(start_period, start_period + width_periods):
                    period_name = TimeConstants.PERIODS_MAPPING.get(period)
                    if period_name:
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