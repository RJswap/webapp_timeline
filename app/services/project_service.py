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
    def create_project(name: str) -> Project:
        project = Project(name=name)
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
        etp: float = 1.0
    ) -> Task:
        task = Task(
            project_id=project_id,
            text=text,
            start_date=start_date,
            end_date=end_date,
            color=color,
            etp=etp
        )
        db.session.add(task)
        db.session.commit()
        return task
    
    @staticmethod
    def update_task(
        task_id: int,
        text: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        color: Optional[str] = None,
        etp: Optional[float] = None
    ) -> Optional[Task]:
        task = Task.query.get(task_id)
        if not task:
            return None
            
        if text is not None:
            task.text = text
        if start_date is not None:
            task.start_date = start_date
        if end_date is not None:
            task.end_date = end_date
        if color is not None:
            task.color = color
        if etp is not None:
            task.etp = etp
            
        db.session.commit()
        return task
    
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

