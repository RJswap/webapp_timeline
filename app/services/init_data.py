from datetime import date
from typing import List, Dict
from app import db
from app.models import Project, Task

def init_db_data():
    """Initialise les données dans la base de données."""
    projects_data = [
        {
            "name": "Procurement",
            "tasks": [
                {
                    "text": "Contrats & RFI",
                    "start_date": date(2025,3,1),
                    "end_date": date(2025, 5, 1),
                    "color": "blue-600",
                    "etp": 1.0
                },
                {
                    "text": "RFP & Négociations",
                    "start_date": date(2025,5,1),
                    "end_date": date(2025, 9, 1),
                    "color": "blue-500",
                    "etp": 1.0
                }
            ]
        },
        {
            "name": "Workforce & HR",
            "tasks": [
                {
                    "text": "Initiation",
                    "start_date": date(2025,3,1),
                    "end_date": date(2025, 5, 1),
                    "color": "purple-600",
                    "etp": 1.0
                },
                {
                    "text": "Analyse & Design",
                    "start_date": date(2025,5,1),
                    "end_date": date(2025, 9, 1),
                    "color": "purple-500",
                    "etp": 1.0
                },
                {
                    "text": "Accompagnement & Déploiement",
                    "start_date": date(2025,9,1),
                    "end_date": date(2027, 12, 30),
                    "color": "purple-400",
                    "etp": 1.0
                }
            ]
        },
        {
            "name": "EUS",
            "tasks": [
                {
                    "text": "Due Diligence",
                    "start_date": date(2025,2,1),
                    "end_date": date(2025, 5, 1),
                    "color": "green-600",
                    "etp": 1.0
                },
                {
                    "text": "RFP",
                    "start_date": date(2025,5,1),
                    "end_date": date(2025, 9, 1),
                    "color": "green-500",
                    "etp": 3.0  # Noté comme "3 ETP" dans les données originales
                },
                {
                    "text": "Pilot & Deploy",
                    "start_date": date(2025,9,1),
                    "end_date": date(2025, 12, 30),
                    "color": "green-400",
                    "etp": 1.0
                }
            ]
        },
        {
            "name": "VIP/Events",
            "tasks": [
                {
                    "text": "Analyse & Design",
                    "start_date": date(2025,3,1),
                    "end_date": date(2025, 5, 1),
                    "color": "yellow-600",
                    "etp": 1.0
                }
            ]
        },
        {
            "name": "Employee Experience",
            "tasks": [
                {
                    "text": "Benchmark & Design",
                    "start_date": date(2025,3,1),
                    "end_date": date(2025, 5, 1),
                    "color": "red-600",
                    "etp": 1.0
                },
                {
                    "text": "Implementation & Optimization",
                    "start_date": date(2025,5,1),
                    "end_date": date(2025, 9, 1),
                    "color": "red-500",
                    "etp": 1.0
                }
            ]
        },
        {
            "name": "Process Data Analytics",
            "tasks": [
                {
                    "text": "Audit & Roadmap",
                    "start_date": date(2025,2,1),
                    "end_date": date(2025, 4, 30),
                    "color": "indigo-600",
                    "etp": 1.0
                },
                {
                    "text": "Implementation & Migration",
                    "start_date": date(2025,5,1),
                    "end_date": date(2025, 6, 30),
                    "color": "indigo-500",
                    "etp": 1.0
                }
            ]
        },
        {
            "name": "Observability",
            "tasks": [
                {
                    "text": "Strategy & Design",
                    "start_date": date(2025,2,1),
                    "end_date": date(2025, 4, 30),
                    "color": "teal-600",
                    "etp": 1.0
                },
                {
                    "text": "POC & Implementation",
                    "start_date": date(2025,5,1),
                    "end_date": date(2025, 6, 30),
                    "color": "teal-500",
                    "etp": 1.0
                }
            ]
        },
        {
            "name": "TOM",
            "tasks": [
                {
                    "text": "Analysis & Design",
                    "start_date": date(2025,2,1),
                    "end_date": date(2025, 4, 30),
                    "color": "gray-600",
                    "etp": 1.0
                },
                {
                    "text": "Implementation & Transition",
                    "start_date": date(2025,5,1),
                    "end_date": date(2025, 6, 30),
                    "color": "gray-500",
                    "etp": 1.0
                }
            ]
        }
    ]

    try:
        # Création des projets et de leurs tâches
        for project_data in projects_data:
            # Créer le projet
            project = Project(name=project_data["name"])
            db.session.add(project)
            db.session.flush()  # Pour obtenir l'ID du projet
            
            # Créer les tâches associées
            for task_data in project_data["tasks"]:
                task = Task(
                    project_id=project.id,
                    text=task_data["text"],
                    start_date=task_data["start_date"],
                    end_date=task_data["end_date"],
                    color=task_data["color"],
                    etp=task_data["etp"]
                )
                db.session.add(task)
        
        # Commit de toutes les modifications
        db.session.commit()
        print("Données initiales chargées avec succès")
        
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de l'initialisation des données : {str(e)}")
        raise