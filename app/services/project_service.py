from typing import List
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
                    Task(start=2, width=2, color="blue-600", text="Analyse contrats & RFI"),
                    Task(start=4, width=2, color="blue-500", text="RFP & Négociations")
                ]
            ),
             Project(
                name="Workforce & HR",
                tasks=[
                    Task(start=1, width=1, color="purple-600", text="Initiation"),
                    Task(start=2, width=2, color="purple-500", text="Analyse & Design"),
                    Task(start=4, width=3, color="purple-400", text="Accompagnement & Déploiement")
                ]
            ),
            Project(
                name="EUS",
                tasks=[
                    Task(start=2, width=2, color="green-600", text="Due Diligence"),
                    Task(start=4, width=1, color="green-500", text="RFP (3 ETP)"),
                    Task(start=5, width=2, color="green-400", text="Pilot & Deploy")
                ]
            ),
            Project(
                name="VIP/Events",
                tasks=[
                    Task(start=1, width=2, color="yellow-600", text="Analyse & Design")
                ]
            ),
            Project(
                name="Employee Experience",
                tasks=[
                    Task(start=2, width=2, color="red-600", text="Benchmark & Design"),
                    Task(start=4, width=3, color="red-500", text="Implementation & Optimization")
                ]
            ),
            Project(
                name="Process Data Analytics",
                tasks=[
                    Task(start=2, width=2, color="indigo-600", text="Audit & Roadmap"),
                    Task(start=4, width=3, color="indigo-500", text="Implementation & Migration")
                ]
            ),
            Project(
                name="Observability",
                tasks=[
                    Task(start=2, width=2, color="teal-600", text="Strategy & Design"),
                    Task(start=4, width=3, color="teal-500", text="POC & Implementation")
                ]
            ),
            Project(
                name="TOM",
                tasks=[
                    Task(start=2, width=2, color="gray-600", text="Analysis & Design"),
                    Task(start=4, width=3, color="gray-500", text="Implementation & Transition")
                ]
            )
        ]
    
        for project in projects:
                for task in project.tasks:
                    stored_etp = EtpService.get_task_etp(project.name, task.start, task.etp or 1.0)
                    task.text = f"{task.text} ({stored_etp} ETP)"
                    task.etp = stored_etp

        return projects