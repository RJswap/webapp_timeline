from dataclasses import dataclass
from typing import List
from .task import Task

@dataclass
class Project:
    name: str
    tasks: List[Task]
    
    def to_dict(self):
        return {
            'name': self.name,
            'tasks': [task.to_dict() for task in self.tasks]
        }