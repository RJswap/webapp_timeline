from typing import List
from app.models.project import Project
from app.models.task import Task

class ProjectService:
    @staticmethod
    def get_all_projects() -> List[Project]:
        # Cette fonction pourrait plus tard récupérer les données depuis une base de données
        return [
            Project(
                name="Procurement",
                tasks=[
                    Task(start=2, width=2, color="blue-600", text="Analyse contrats & RFI (1 ETP)"),
                    Task(start=4, width=2, color="blue-500", text="RFP & Négociations (1 ETP)")
                ]
            ),
             Project(
                name="Workforce & HR",
                tasks=[
                    Task(start=1, width=1, color="purple-600", text="Initiation (1 ETP)"),
                    Task(start=2, width=2, color="purple-500", text="Analyse & Design (2 ETP)"),
                    Task(start=4, width=3, color="purple-400", text="Accompagnement & Déploiement (2 ETP)")
                ]
            ),
            Project(
                name="EUS",
                tasks=[
                    Task(start=2, width=2, color="green-600", text="Due Diligence (3 ETP)"),
                    Task(start=4, width=1, color="green-500", text="RFP (3 ETP)"),
                    Task(start=5, width=2, color="green-400", text="Pilot & Deploy (3 ETP)")
                ]
            ),
            Project(
                name="VIP/Events",
                tasks=[
                    Task(start=1, width=2, color="yellow-600", text="Analyse & Design (0.5 ETP)")
                ]
            ),
            Project(
                name="Employee Experience",
                tasks=[
                    Task(start=2, width=2, color="red-600", text="Benchmark & Design (2 ETP)"),
                    Task(start=4, width=3, color="red-500", text="Implementation & Optimization (2 ETP)")
                ]
            ),
            Project(
                name="Process Data Analytics",
                tasks=[
                    Task(start=2, width=2, color="indigo-600", text="Audit & Roadmap (3 ETP)"),
                    Task(start=4, width=3, color="indigo-500", text="Implementation & Migration (3 ETP)")
                ]
            ),
            Project(
                name="Observability",
                tasks=[
                    Task(start=2, width=2, color="teal-600", text="Strategy & Design (2 ETP)"),
                    Task(start=4, width=3, color="teal-500", text="POC & Implementation (2 ETP)")
                ]
            ),
            Project(
                name="TOM",
                tasks=[
                    Task(start=2, width=2, color="gray-600", text="Analysis & Design (2 ETP)"),
                    Task(start=4, width=3, color="gray-500", text="Implementation & Transition (2 ETP)")
                ]
            )
        ]