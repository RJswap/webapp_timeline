from typing import List
from datetime import date
from app.models.project import Project
from app.models.task import Task
from app.services.etp_service import EtpService

class ProjectService:
    @staticmethod
    def get_all_projects() -> List[Project]:
        # Cette fonction pourrait plus tard récupérer les données depuis une base de données
        projects = [
            Project(
                name="Procurement",
                tasks=[
                    Task(start_date=date(2025,3,1), end_date=date(2025, 5, 1), color="blue-600", text="Contrats & RFI"),
                    Task(start_date=date(2025,5,1), end_date=date(2025, 9, 1), color="blue-500", text="RFP & Négociations")
                ]
            ),
             Project(
                name="Workforce & HR",
                tasks=[
                    Task(start_date=date(2025,3,1), end_date=date(2025, 5, 1), color="purple-600", text="Initiation"),
                    Task(start_date=date(2025,5,1), end_date=date(2025, 9, 1), color="purple-500", text="Analyse & Design"),
                    Task(start_date=date(2025,9,1), end_date=date(2027, 12, 30), color="purple-400", text="Accompagnement & Déploiement")
                ]
            ),
            Project(
                name="EUS",
                tasks=[
                    Task(start_date=date(2025,2,1), end_date=date(2025, 5, 1), color="green-600", text="Due Diligence"),
                    Task(start_date=date(2025,5,1), end_date=date(2025, 9, 1), color="green-500", text="RFP (3 ETP)"),
                    Task(start_date=date(2025,9,1), end_date=date(2025, 12, 30), color="green-400", text="Pilot & Deploy")
                ]
            ),
            Project(
                name="VIP/Events",
                tasks=[
                    Task(start_date=date(2025,3,1), end_date=date(2025, 5, 1), color="yellow-600", text="Analyse & Design")
                ]
            ),
            Project(
                name="Employee Experience",
                tasks=[
                    Task(start_date=date(2025,3,1), end_date=date(2025, 5, 1), color="red-600", text="Benchmark & Design"),
                    Task(start_date=date(2025,5,1), end_date=date(2025, 9, 1), color="red-500", text="Implementation & Optimization")
                ]
            ),
            Project(
                name="Process Data Analytics",
                tasks=[
                    Task(start_date=date(2025,2,1), end_date=date(2025, 4, 30), color="indigo-600", text="Audit & Roadmap"),
                    Task(start_date=date(2025,5,1), end_date=date(2025, 6, 30), color="indigo-500", text="Implementation & Migration")
                ]
            ),
            Project(
                name="Observability",
                tasks=[
                    Task(start_date=date(2025,2,1), end_date=date(2025, 4, 30), color="teal-600", text="Strategy & Design"),
                    Task(start_date=date(2025,5,1), end_date=date(2025, 6, 30), color="teal-500", text="POC & Implementation")
                ]
            ),
            Project(
                name="TOM",
                tasks=[
                    Task(start_date=date(2025,2,1), end_date=date(2025, 4, 30), color="gray-600", text="Analysis & Design"),
                    Task(start_date=date(2025,5,1), end_date=date(2025, 6, 30), color="gray-500", text="Implementation & Transition")
                ]
            )
        ]
    
        for project in projects:
            for task in project.tasks:
                stored_etp = EtpService.get_task_etp_by_date(
                    project.name,
                    task.start_date,
                    task.etp or 1.0
                )
                task.text = f"{task.text} ({stored_etp} ETP)"
                task.etp = stored_etp

        return projects