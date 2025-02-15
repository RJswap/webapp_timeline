from typing import List, Optional
from datetime import date
from app import db
from typing import List, Optional
from datetime import date
from app import db
from app.models import Project, Task
from app.services.etp_service import EtpService
from sqlalchemy.exc import IntegrityError

class ProjectService:
    COLOR_INTENSITIES = ['600', '500', '400']
    @staticmethod
    def get_all_projects() -> List[Project]:
        return Project.query.all()
    
    @staticmethod
    def get_project_by_id(project_id: int) -> Optional[Project]:
        return Project.query.get(project_id)
    
    @staticmethod
    def get_project_by_name(name: str) -> Optional[Project]:
        return Project.query.filter_by(name=name).first()
    
    @staticmethod
    def create_project(name: str, color_scheme: str = 'blue') -> Project:
        project = Project(name=name, color_scheme=color_scheme)
        db.session.add(project)
        try:
            db.session.commit()
            return project
        except IntegrityError:
            db.session.rollback()
            raise ValueError(f"Project with name '{name}' already exists")
    
    @staticmethod
    def create_task(
        project_id: int,
        text: str,
        start_date: date,
        end_date: date,
        color: str,
        etp: float = 1.0,
        comment: str = None
    ) -> Optional[Task]:
        try:
            # Récupérer le projet pour obtenir son schéma de couleur
            project = Project.query.get(project_id)
            if not project:
                raise ValueError("Project not found")

            # Si aucune couleur n'est spécifiée, utiliser le schéma de couleur du projet
            if color is None:
                # Déterminer l'intensité en fonction du nombre de tâches existantes
                intensities = ['600', '500', '400']
                intensity = intensities[len(project.tasks) % len(intensities)]
                color = f"{project.color_scheme}-{intensity}"

            print(f"Creating task in service: {project_id}, {text}, {start_date}-{end_date}, {color}")
            task = Task(
                project_id=project_id,
                text=text,
                comment=comment,
                start_date=start_date,
                end_date=end_date,
                color=color,
                etp=etp
            )
            
            db.session.add(task)
            db.session.commit()
            
            # Vérifier que la tâche a bien été créée
            created_task = Task.query.get(task.id)
            if created_task:
                print(f"Task created successfully with ID: {created_task.id}")
                return created_task
            else:
                print("Task was not created properly")
                return None
                
        except Exception as e:
            print(f"Error in create_task: {str(e)}")
            db.session.rollback()
            raise
    
    @staticmethod
    def delete_task(task_id: int) -> bool:
        task = Task.query.get(task_id)
        if not task:
            return False
            
        db.session.delete(task)
        db.session.commit()
        return True
    
    @staticmethod
    def delete_project(project_id: int) -> bool:
        project = Project.query.get(project_id)
        if not project:
            return False
            
        db.session.delete(project)
        db.session.commit()
        return True

