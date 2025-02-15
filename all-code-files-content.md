### constants.py
```py
class TimeConstants:
    PERIODS_MAPPING = {
        1: "2025 Q1-Q2",
        2: "2025 Q3-Q4",
        3: "2026-2027"
    }
    
    PERIODS_DISPLAY = [
        "2025 Q1",
        "2025 Q2",
        "2025 Q3",
        "2025 Q4",
        "2026-2027"
    ]
    
    MILESTONES = [
        {"position": "left-1/3", "text": "RFI"},
        {"position": "left-1/2", "text": "RFP"},
        {"position": "left-2/3", "text": "Pilot"},
        {"position": "right-1/6", "text": "Déploiement"}
    ]
```

### base.html
```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Danone{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/normalize.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/base.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/etp_table.css') }}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="main-nav">
        <div class="nav-content">
            <a href="{{ url_for('main.index') }}" class="logo">Danone</a>
            <ul class="nav-links">
                <li><a href="{{ url_for('project.timeline') }}">Timeline</a></li>
                <li><a href="{{ url_for('project.etp_table') }}">ETP</a></li>
            </ul>
        </div>
    </nav>

    <main class="main-content">
        {% block content %}{% endblock %}
    </main>

    

    <script src="{{ url_for('static', filename='js/base.js') }}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>

```

### base.js
```js
// base.js - Fonctionnalités communes à toute l'application

document.addEventListener('DOMContentLoaded', function() {
    // Configuration des variables globales
    window.APP = {
        config: {
            animationDuration: 300,
            dateFormat: 'DD/MM/YYYY',
            apiEndpoint: '/api'
        }
    };

    // Gestion de la navigation active
    const handleActiveNavigation = () => {
        const currentPath = window.location.pathname;
        document.querySelectorAll('.nav-links a').forEach(link => {
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            }
        });
    };

    // Gestion des notifications
    const notifications = {
        container: null,
        
        init() {
            this.container = document.createElement('div');
            this.container.className = 'notifications-container';
            document.body.appendChild(this.container);
        },

        show(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `notification notification-${type}`;
            notification.textContent = message;
            
            this.container.appendChild(notification);
            
            // Animation d'entrée
            setTimeout(() => {
                notification.classList.add('show');
            }, 10);

            // Auto-suppression après 5 secondes
            setTimeout(() => {
                notification.classList.remove('show');
                setTimeout(() => {
                    notification.remove();
                }, 300);
            }, 5000);
        }
    };

    // Gestion du thème
    const themeManager = {
        init() {
            const savedTheme = localStorage.getItem('theme') || 'light';
            this.setTheme(savedTheme);
            
            // Écouteur pour le bouton de changement de thème (si présent)
            const themeToggle = document.querySelector('.theme-toggle');
            if (themeToggle) {
                themeToggle.addEventListener('click', () => {
                    const newTheme = document.body.classList.contains('dark-theme') ? 'light' : 'dark';
                    this.setTheme(newTheme);
                });
            }
        },

        setTheme(theme) {
            document.body.classList.remove('light-theme', 'dark-theme');
            document.body.classList.add(`${theme}-theme`);
            localStorage.setItem('theme', theme);
        }
    };

    // Utilitaires pour les dates
    const dateUtils = {
        formatDate(date) {
            return new Intl.DateTimeFormat('fr-FR').format(date);
        },

        formatDateTime(date) {
            return new Intl.DateTimeFormat('fr-FR', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            }).format(date);
        }
    };

    // Gestion des formulaires
    const formManager = {
        init() {
            document.querySelectorAll('form').forEach(form => {
                form.addEventListener('submit', this.handleSubmit.bind(this));
            });
        },

        handleSubmit(event) {
            const form = event.target;
            
            // Désactiver le bouton submit pendant le traitement
            const submitButton = form.querySelector('[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
            }

            // Réactiver le bouton après le traitement
            setTimeout(() => {
                if (submitButton) {
                    submitButton.disabled = false;
                }
            }, 1000);
        },

        validateForm(form) {
            let isValid = true;
            const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    this.showError(input, 'Ce champ est requis');
                } else {
                    this.clearError(input);
                }
            });

            return isValid;
        },

        showError(input, message) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'form-error';
            errorDiv.textContent = message;
            input.classList.add('error');
            input.parentNode.appendChild(errorDiv);
        },

        clearError(input) {
            input.classList.remove('error');
            const errorDiv = input.parentNode.querySelector('.form-error');
            if (errorDiv) {
                errorDiv.remove();
            }
        }
    };

    // Gestion des erreurs globales
    //window.onerror = function(msg, url, lineNo, columnNo, error) {
        //console.error('Error: ', msg, url, lineNo, columnNo, error);
        //notifications.show('Une erreur est survenue', 'error');
        //return false;
    //};

    // Initialisation des composants
    const init = () => {
        handleActiveNavigation();
        notifications.init();
        themeManager.init();
        formManager.init();
        
        // Exposer les utilitaires globalement
        window.APP = {
            ...window.APP,
            notifications,
            dateUtils,
            formManager
        };
    };

    // Lancer l'initialisation
    init();
});
```

### __init__.py
```py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import DevelopmentConfig

db = SQLAlchemy()
migrate_manager = Migrate()  # Renommé pour éviter le conflit

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize database
    db.init_app(app)
    
    # Initialize Flask-Migrate
    migrate_manager.init_app(app, db)
    
    # Register blueprints
    from app.routes import main, project
    app.register_blueprint(main)
    app.register_blueprint(project)
    
    return app
```

### __init__.py
```py
from .project_service import ProjectService
from .etp_service import EtpService

__all__ = ['ProjectService', 'EtpService']
```

### timeline.js
```js
// Gestionnaire de la timeline
const TimelineManager = {
    init() {
        this.timelineRows = document.querySelectorAll('.timeline-row');
        this.setupStreamToggles();
        this.validateTaskPositions();
        this.setupProjectButtons();
        this.setupTaskButtons();
    },

    setupStreamToggles() {
        const streamToggles = document.createElement('div');
        streamToggles.className = 'stream-toggles';
        
        this.timelineRows.forEach((row) => {
            const toggleWrapper = this.createToggle(row);
            streamToggles.appendChild(toggleWrapper);
        });
        
        const timelineContainer = document.querySelector('.timeline-container');
        timelineContainer.insertBefore(streamToggles, timelineContainer.querySelector('.timeline-grid'));
    },

    setupProjectButtons() {
        // Gérer le bouton "Nouveau Projet"
        const addProjectBtn = document.getElementById('addProjectBtn');
        if (addProjectBtn) {
            addProjectBtn.addEventListener('click', () => {
                ModalManager.openNewProjectModal();
            });
        }

        // Gérer les clics sur les noms de projets
        document.querySelectorAll('.project-name').forEach(projectName => {
            projectName.addEventListener('click', (e) => {
                e.preventDefault();
                const projectId = projectName.closest('.timeline-row').dataset.projectId;
                const projectTitle = projectName.textContent.trim();
                const colorScheme = projectName.closest('.timeline-row').dataset.colorScheme || 'blue';
                ModalManager.openProjectEditModal(projectId, projectTitle, colorScheme);
            });
        });
    },

    createToggle(row) {
        const projectName = row.dataset.projectName;
        const toggleWrapper = document.createElement('div');
        toggleWrapper.className = 'stream-toggle';
        
        const label = document.createElement('label');
        label.className = 'switch';
        
        const input = document.createElement('input');
        input.type = 'checkbox';
        input.checked = true;
        
        const slider = document.createElement('span');
        slider.className = 'slider';
        
        label.appendChild(input);
        label.appendChild(slider);
        
        const nameLabel = document.createElement('span');
        nameLabel.textContent = projectName;
        
        toggleWrapper.appendChild(label);
        toggleWrapper.appendChild(nameLabel);
        
        input.addEventListener('change', () => {
            this.toggleRowVisibility(row, input.checked);
            this.updatePositions();
        });
        
        return toggleWrapper;
    },

    toggleRowVisibility(row, isVisible) {
        if (isVisible) {
            row.classList.remove('hidden');
            row.style.height = '';
            row.style.opacity = '1';
        } else {
            row.classList.add('hidden');
            row.style.height = '0';
            row.style.opacity = '0';
        }
    },

    updatePositions() {
        let currentOffset = 0;
        this.timelineRows.forEach(row => {
            if (!row.classList.contains('hidden')) {
                currentOffset += row.offsetHeight + 16;
            }
        });
    },

    validateTaskPositions() {
        document.querySelectorAll('.task').forEach(task => {
            const left = task.style.left;
            const width = task.style.width;
            task.title = `Position: ${left} | Width: ${width}`;
        });
    },

    setupTaskButtons() {
        // Gestionnaire pour le bouton "Nouvelle Tâche"
        const addTaskBtn = document.getElementById('addTaskBtn');
        if (addTaskBtn) {
            addTaskBtn.addEventListener('click', () => {
                ModalManager.openNewTaskModal();
            });
        }

        // Gestionnaire pour les tâches existantes
        document.querySelectorAll('.task').forEach(task => {
            task.addEventListener('click', (e) => {
                e.stopPropagation();
                const taskData = {
                    id: task.dataset.taskId,
                    projectId: task.closest('.timeline-row').dataset.projectId,
                    text: task.dataset.taskInfo,
                    startDate: task.dataset.startDate,
                    endDate: task.dataset.endDate,
                    etp: task.dataset.etp
                };
                ModalManager.openEditTaskModal(taskData);
            });
        });
    }
};


// Gestionnaire des modals
const ModalManager = {
    init() {
        this.initElements();
        this.setupEventListeners();
        this.setupProjectHandlers();
        this.setupTaskHandlers();
        this.initializeDateInputs();
    },

    initElements() {
        this.elements = {
            newProjectModal: document.getElementById('newProjectModal'),
            newTaskModal: document.getElementById('newTaskModal'),
            editTaskModal: document.getElementById('editTaskModal'),
            projectForm: document.getElementById('projectForm'),
            taskForm: document.getElementById('newTaskForm'),
            editTaskForm: document.getElementById('editTaskForm'),
            deleteTaskBtn: document.getElementById('deleteTaskBtn'),
            deleteProjectBtn: document.getElementById('deleteProjectBtn'),
            projectModalTitle: document.getElementById('projectModalTitle'),
            submitProjectBtn: document.getElementById('submitProjectBtn'),
            taskProjectSelect: document.getElementById('taskProject'),
            editTaskProjectSelect: document.getElementById('editTaskProject'),
            deleteTaskBtn: document.getElementById('deleteTaskBtn')
        };
    },

    setupEventListeners() {
        // Gestionnaires de fermeture des modals
        document.querySelectorAll('.close, .close-modal').forEach(element => {
            element.addEventListener('click', () => this.closeAllModals());
        });

        // Gestionnaire du formulaire de projet
        if (this.elements.projectForm) {
            this.elements.projectForm.addEventListener('submit', (e) => this.handleProjectSubmit(e));
        }

        // Gestion des formulaires de tâches
        if (this.elements.taskForm) {
            this.elements.taskForm.addEventListener('submit', (e) => this.handleTaskSubmit(e));
        }

        if (this.elements.editTaskForm) {
            this.elements.editTaskForm.addEventListener('submit', (e) => this.handleEditTaskSubmit(e));
        }

        if (this.elements.deleteTaskBtn) {
            this.elements.deleteTaskBtn.addEventListener('click', () => this.handleTaskDelete());
        }

        // Gestionnaire du bouton de suppression de projet
        if (this.elements.deleteProjectBtn) {
            this.elements.deleteProjectBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleProjectDelete();
            });
        }
    },

    
    openNewProjectModal() {
        const modal = this.elements.newProjectModal;
        if (!modal) return;

        // Reset du formulaire
        this.elements.projectForm.reset();
        document.getElementById('projectId').value = '';
        
        // Mise à jour du titre et des boutons
        this.elements.projectModalTitle.textContent = 'Nouveau Projet';
        this.elements.submitProjectBtn.textContent = 'Créer';
        this.elements.deleteProjectBtn.style.display = 'none';

        modal.classList.add('show');
    },

    openProjectEditModal(projectId, projectName, colorScheme) {
        const modal = this.elements.newProjectModal;
        if (!modal) return;

        // Mise à jour du titre
        this.elements.projectModalTitle.textContent = 'Modifier le Projet';

        // Remplissage du formulaire
        document.getElementById('projectId').value = projectId;
        document.getElementById('projectName').value = projectName;
        document.getElementById('colorScheme').value = colorScheme;

        // Affichage du bouton de suppression et mise à jour du bouton de soumission
        this.elements.deleteProjectBtn.style.display = 'block';
        this.elements.submitProjectBtn.textContent = 'Modifier';

        modal.classList.add('show');
    },

    async handleProjectSubmit(e) {
        e.preventDefault();
        const formData = new FormData(this.elements.projectForm);
        const projectId = document.getElementById('projectId').value;
        const method = projectId ? 'PUT' : 'POST';
        const url = projectId ? `/project/api/projects/${projectId}` : '/project/api/projects';

        try {
            const response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(Object.fromEntries(formData))
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Erreur lors de l\'opération sur le projet');
            }

            window.location.reload();
        } catch (error) {
            console.error('Error:', error);
            alert(error.message);
        }
    },

    async handleProjectDelete() {
        const projectId = document.getElementById('projectId').value;
        const projectName = document.getElementById('projectName').value;

        if (confirm(`Êtes-vous sûr de vouloir supprimer le projet "${projectName}" ?\nCette action supprimera également toutes les tâches associées.`)) {
            try {
                const response = await fetch(`/project/api/projects/${projectId}`, {
                    method: 'DELETE'
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Erreur lors de la suppression du projet');
                }

                window.location.reload();
            } catch (error) {
                console.error('Error:', error);
                alert(error.message);
            }
        }
    },

    initializeDateInputs() {
        const dateInputs = document.querySelectorAll('input[type="date"]');
        const today = new Date().toISOString().split('T')[0];
        
        dateInputs.forEach(input => {
            input.min = today;
            
            // Pour les inputs de date de fin, mettre à jour le min quand la date de début change
            if (input.id.includes('End')) {
                const startInput = document.getElementById(input.id.replace('End', 'Start'));
                if (startInput) {
                    startInput.addEventListener('change', () => {
                        input.min = startInput.value;
                        if (input.value && input.value < startInput.value) {
                            input.value = startInput.value;
                        }
                    });
                }
            }
        });
    },

    openNewTaskModal() {
        const modal = this.elements.newTaskModal;
        if (!modal) return;

        this.elements.taskForm.reset();
        this.updateProjectSelect();
        modal.classList.add('show');
    },

    openEditTaskModal(taskData) {
        const modal = this.elements.editTaskModal;
        if (!modal) return;

        // Remplir le formulaire avec les données de la tâche
        document.getElementById('editTaskId').value = taskData.id;
        document.getElementById('editTaskProject').value = taskData.projectId;
        document.getElementById('editTaskText').value = taskData.text;
        document.getElementById('editTaskStartDate').value = taskData.startDate;
        document.getElementById('editTaskEndDate').value = taskData.endDate;
        document.getElementById('editTaskEtp').value = taskData.etp;

        modal.classList.add('show');
    },

    async handleTaskSubmit(e) {
        e.preventDefault();
        const formData = new FormData(this.elements.taskForm);
        
        try {
            const response = await fetch('/project/api/tasks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(Object.fromEntries(formData))
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Erreur lors de la création de la tâche');
            }

            window.location.reload();
        } catch (error) {
            console.error('Error:', error);
            alert(error.message);
        }
    },

    async handleEditTaskSubmit(e) {
        e.preventDefault();
        const formData = new FormData(this.elements.editTaskForm);
        const taskId = formData.get('task_id');
        
        try {
            const response = await fetch(`/project/api/tasks/${taskId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(Object.fromEntries(formData))
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Erreur lors de la modification de la tâche');
            }

            window.location.reload();
        } catch (error) {
            console.error('Error:', error);
            alert(error.message);
        }
    },

    async handleTaskDelete() {
        const taskId = document.getElementById('editTaskId').value;
        const taskText = document.getElementById('editTaskText').value;
        
        if (confirm(`Êtes-vous sûr de vouloir supprimer la tâche "${taskText}" ?`)) {
            try {
                const response = await fetch(`/project/api/tasks/${taskId}`, {
                    method: 'DELETE'
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Erreur lors de la suppression de la tâche');
                }

                window.location.reload();
            } catch (error) {
                console.error('Error:', error);
                alert(error.message);
            }
        }
    },

    async updateProjectSelect() {
        try {
            const response = await fetch('/project/api/projects');
            if (!response.ok) throw new Error('Erreur lors de la récupération des projets');
            
            const data = await response.json();
            
            [this.elements.taskProjectSelect, this.elements.editTaskProjectSelect].forEach(select => {
                if (select) {
                    select.innerHTML = '';
                    data.data.projects.forEach(project => {
                        const option = document.createElement('option');
                        option.value = project.id;
                        option.textContent = project.name;
                        select.appendChild(option);
                    });
                }
            });
        } catch (error) {
            console.error('Error updating project selects:', error);
            alert('Erreur lors de la mise à jour de la liste des projets');
        }
    },

    closeAllModals() {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.classList.remove('show');
        });
    },

    // ... Le reste du code pour la gestion des tâches reste inchangé
};

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    TimelineManager.init();
    ModalManager.init();
});
```

### project_service.py
```py
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
        etp: float = 1.0
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


```

### init_data.py
```py
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
```

### etp_table.js
```js
// static/js/project/etp_table.js

document.addEventListener('DOMContentLoaded', function() {
    const table = document.querySelector('.etp-table');
    let activeInput = null;

    // Gérer le clic sur une cellule éditable
    document.addEventListener('click', function(e) {
        const cell = e.target.closest('.editable-cell');
        if (!cell) return;
        if (cell.querySelector('input')) return;

        const valueSpan = cell.querySelector('.etp-value');
        const currentValue = valueSpan.textContent.trim();

        const input = document.createElement('input');
        input.type = 'number';
        input.step = '0.1';
        input.min = '0';
        input.value = currentValue;
        input.className = 'etp-input';

        valueSpan.style.display = 'none';
        cell.appendChild(input);
        input.focus();
        activeInput = input;

        input.select();
    });

    // Gérer la validation des modifications
    async function saveChange(cell, newValue) {
        const project = cell.closest('tr').dataset.project;
        const period = cell.dataset.period;

        try {
            const response = await fetch('/project/api/update_etp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    project,
                    period,
                    etp: newValue
                })
            });

            if (!response.ok) throw new Error('Failed to update ETP');

            const valueSpan = cell.querySelector('.etp-value');
            valueSpan.textContent = parseFloat(newValue).toFixed(2);
            valueSpan.style.display = '';
            valueSpan.classList.add('updated');
            
            if (cell.querySelector('input')) {
                cell.querySelector('input').remove();
            }

            updateTotals();
            
        } catch (error) {
            console.error('Error updating ETP:', error);
            alert('Failed to update ETP');
        }
    }

    // Gérer les touches clavier pendant l'édition
    document.addEventListener('keydown', function(e) {
        if (!activeInput) return;
        
        if (e.key === 'Enter') {
            e.preventDefault();
            const newValue = activeInput.value;
            if (newValue && !isNaN(newValue)) {
                const cell = activeInput.closest('.editable-cell');
                saveChange(cell, newValue);
            }
            activeInput = null;
        } else if (e.key === 'Escape') {
            const cell = activeInput.closest('.editable-cell');
            cell.querySelector('.etp-value').style.display = '';
            activeInput.remove();
            activeInput = null;
        }
    });

    // Gérer la perte de focus
    document.addEventListener('click', function(e) {
        if (activeInput && !activeInput.contains(e.target) && !e.target.closest('.editable-cell')) {
            const newValue = activeInput.value;
            if (newValue && !isNaN(newValue)) {
                const cell = activeInput.closest('.editable-cell');
                saveChange(cell, newValue);
            }
            activeInput = null;
        }
    });

    // Fonction pour mettre à jour tous les totaux
    function updateTotals() {
        // Totaux par période
        const periods = ['2025 Q1-Q2', '2025 Q3-Q4', '2026-2027'];
        
        periods.forEach(period => {
            const cells = table.querySelectorAll(`td[data-period="${period}"] .etp-value`);
            const total = Array.from(cells)
                .reduce((sum, cell) => sum + parseFloat(cell.textContent || 0), 0);
            const totalCell = table.querySelector(`.period-total[data-period="${period}"]`);
            if (totalCell) {
                totalCell.textContent = total.toFixed(2);
                totalCell.classList.add('updated');
            }
        });

        // Totaux par ligne (max ETP)
        const projectRows = table.querySelectorAll('tr[data-project]');
        projectRows.forEach(row => {
            const etpCells = row.querySelectorAll('.etp-value');
            const maxEtp = Array.from(etpCells)
                .reduce((max, cell) => Math.max(max, parseFloat(cell.textContent || 0)), 0);
            const totalCell = row.querySelector('.row-total');
            if (totalCell) {
                totalCell.textContent = maxEtp.toFixed(2);
                totalCell.classList.add('updated');
            }
        });

        // Total général (somme des max ETP)
        const rowTotals = Array.from(table.querySelectorAll('.row-total'))
            .map(cell => parseFloat(cell.textContent || 0));
        const grandTotal = rowTotals.reduce((sum, val) => sum + val, 0);
        const grandTotalCell = table.querySelector('.grand-total');
        if (grandTotalCell) {
            grandTotalCell.textContent = grandTotal.toFixed(2);
            grandTotalCell.classList.add('updated');
        }

        // Retirer les classes 'updated' après l'animation
        setTimeout(() => {
            table.querySelectorAll('.updated').forEach(el => {
                el.classList.remove('updated');
            });
        }, 1000);
    }
});
```

### etp_service.py
```py
from collections import defaultdict
from typing import List, Dict, Tuple
from datetime import date, datetime
from app import db
from app.models import Project, EtpEntry
from app.constants import TimeConstants

class EtpService:
    @staticmethod
    def get_stored_etp(project_id: int, period: str) -> float:
        """Récupère la valeur ETP stockée pour un projet et une période donnés"""
        entry = EtpEntry.query.filter_by(
            project_id=project_id,
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
    def get_task_etp_by_date(project_id: int, task_date: date, default_etp: float) -> float:
        """Récupère l'ETP pour une tâche à une date spécifique"""
        period = EtpService.get_period_for_date(task_date)
        stored_etp = EtpService.get_stored_etp(project_id, period)
        return stored_etp if stored_etp is not None else default_etp

    @staticmethod
    def calculate_etp_per_period(projects: List[Project]) -> Tuple[List[Dict], Dict[str, float]]:
        etp_data = []
        period_totals = defaultdict(float)
        
        for project in projects:
            project_etps = defaultdict(float)
            max_etp = 0
            
            stored_etps = EtpEntry.query.filter_by(project_id=project.id).all()
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
    def update_etp(project_id: int, period: str, etp_value: float) -> None:
        """Update ETP value in database"""
        entry = EtpEntry.query.filter_by(
            project_id=project_id,
            period=period
        ).first()
        
        if entry:
            entry.etp_value = etp_value
            entry.updated_at = datetime.utcnow()
        else:
            entry = EtpEntry(
                project_id=project_id,
                period=period,
                etp_value=etp_value
            )
            db.session.add(entry)
            
        db.session.commit()
```

### timeline.html
```html
{% extends "base.html" %}

{% block title %}Timeline - Project Manager{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/timeline.css') }}">
{% endblock %}

{% block content %}
    <div class="timeline-container">
        <h1 class="page-title">Project Timeline</h1>
        
        <!-- Boutons d'action -->
        <div class="action-buttons">
            <button id="addProjectBtn" class="btn-primary">
                <i class="fas fa-plus"></i> Nouveau Projet
            </button>
            <button id="addTaskBtn" class="btn-primary">
                <i class="fas fa-plus"></i> Nouvelle Tâche
            </button>
        </div>
        
        <div class="timeline-grid">
            <div class="timeline-main">
                <div class="periods-grid">
                    <div class="period"></div>
                    {% for period in periods %}
                    <div class="period">{{ period }}</div>
                    {% endfor %}
                </div>

                <div class="timeline-rows-container">
                    {% for project in projects %}
                    <div class="timeline-row" 
                         data-project-name="{{ project.name }}" 
                         data-project-id="{{ project.id }}"
                         data-color-scheme="{{ project.color_scheme }}">
                        <div class="project-name">{{ project.name }}</div>
                        <div class="project-tasks">
                            {% for task in project.tasks %}
                            <div class="task bg-{{ task.color }}"
                                style="left: {{ task.start }}%; width: {{ task.width }}%;"
                                data-task-id="{{ task.id }}"
                                data-task-info="{{ task.text }}"
                                data-dates="{{ task.dates }}"
                                data-start-date="{{ task.raw_start_date }}"
                                data-end-date="{{ task.raw_end_date }}"
                                data-etp="{{ task.etp }}">
                                {{ task.text }}
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>

    <div id="newProjectModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="projectModalTitle">Nouveau Projet</h2>
                <span class="close">&times;</span>
            </div>
            <form id="projectForm">
                <input type="hidden" id="projectId" name="project_id" value="">
                
                <div class="form-group">
                    <label for="projectName">Nom du projet</label>
                    <input type="text" id="projectName" name="name" required>
                </div>
                
                <div class="form-group">
                    <label for="colorScheme">Schéma de couleur</label>
                    <select id="colorScheme" name="colorScheme" required>
                        <option value="blue">Bleu</option>
                        <option value="purple">Violet</option>
                        <option value="green">Vert</option>
                        <option value="yellow">Jaune</option>
                        <option value="red">Rouge</option>
                        <option value="indigo">Indigo</option>
                        <option value="teal">Teal</option>
                        <option value="gray">Gris</option>
                    </select>
                </div>
                
                <div class="modal-footer">
                    <button type="button" id="deleteProjectBtn" class="btn-danger" style="display: none;">
                        Supprimer le projet
                    </button>
                    <div class="action-buttons">
                        <button type="submit" id="submitProjectBtn" class="btn-primary">Créer</button>
                        <button type="button" class="btn-secondary close-modal">Annuler</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Modal Nouvelle Tâche -->
    <div id="newTaskModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Nouvelle Tâche</h2>
                <span class="close">&times;</span>
            </div>
            <form id="newTaskForm">
                <div class="form-group">
                    <label for="taskProject">Projet</label>
                    <select id="taskProject" name="project_id" required>
                        <!-- Rempli dynamiquement -->
                    </select>
                </div>
                <div class="form-group">
                    <label for="taskText">Description</label>
                    <input type="text" id="taskText" name="text" required>
                </div>
                <div class="form-group">
                    <label for="taskStartDate">Date de début</label>
                    <input type="date" id="taskStartDate" name="start_date" required>
                </div>
                <div class="form-group">
                    <label for="taskEndDate">Date de fin</label>
                    <input type="date" id="taskEndDate" name="end_date" required>
                </div>
                <div class="form-group">
                    <label for="taskEtp">ETP</label>
                    <input type="number" id="taskEtp" name="etp" step="0.1" min="0" value="1.0" required>
                </div>
                <div class="modal-footer">
                    <button type="submit" class="btn-primary">Créer</button>
                    <button type="button" class="btn-secondary close-modal">Annuler</button>
                </div>
            </form>
        </div>
    </div>

    <div id="editTaskModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Modifier la Tâche</h2>
                <span class="close">&times;</span>
            </div>
            <form id="editTaskForm">
                <input type="hidden" id="editTaskId" name="task_id">
                <div class="form-group">
                    <label for="editTaskProject">Projet</label>
                    <select id="editTaskProject" name="project_id" required disabled>
                        <!-- Rempli dynamiquement -->
                    </select>
                </div>
                <div class="form-group">
                    <label for="editTaskText">Description</label>
                    <input type="text" id="editTaskText" name="text" required>
                </div>
                <div class="form-group">
                    <label for="editTaskStartDate">Date de début</label>
                    <input type="date" id="editTaskStartDate" name="start_date" required>
                </div>
                <div class="form-group">
                    <label for="editTaskEndDate">Date de fin</label>
                    <input type="date" id="editTaskEndDate" name="end_date" required>
                </div>
                <div class="form-group">
                    <label for="editTaskEtp">ETP</label>
                    <input type="number" id="editTaskEtp" name="etp" step="0.1" min="0" required>
                </div>
                <div class="modal-footer">
                    <button type="submit" class="btn-primary">Enregistrer</button>
                    <button type="button" class="btn-danger" id="deleteTaskBtn">Supprimer</button>
                    <button type="button" class="btn-secondary close-modal">Annuler</button>
                </div>
            </form>
        </div>
    </div>
{% endblock %}

{% block extra_js %}
<script src="{{ url_for('static', filename='js/project/timeline.js') }}"></script>
{% endblock %}
```

### etp_table.html
```html
{% extends "base.html" %}

{% block title %}ETP Table - Project Manager{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/project/etp_table.css') }}">
{% endblock %}

{% block content %}
<div class="etp-container">
    <h1 class="page-title">Resource Allocation (ETP)</h1>
    
    <div class="etp-table-container">
        <table class="etp-table">
            <thead>
                <tr>
                    <th>Stream</th>
                    <th>2025 Q1-Q2</th>
                    <th>2025 Q3-Q4</th>
                    <th>2026-2027</th>
                    <th>ETP Total</th>
                </tr>
            </thead>
            <tbody>
                {% for row in etp_data %}
                <tr data-project="{{ row.name }}">
                    <td>{{ row.name }}</td>
                    <td class="text-center editable-cell" data-period="2025 Q1-Q2">
                        <span class="etp-value">{{ "%.2f"|format(row["2025 Q1-Q2"]) }}</span>
                    </td>
                    <td class="text-center editable-cell" data-period="2025 Q3-Q4">
                        <span class="etp-value">{{ "%.2f"|format(row["2025 Q3-Q4"]) }}</span>
                    </td>
                    <td class="text-center editable-cell" data-period="2026-2027">
                        <span class="etp-value">{{ "%.2f"|format(row["2026-2027"]) }}</span>
                    </td>
                    <td class="text-center row-total">{{ "%.2f"|format(row.total) }}</td>
                </tr>
                {% endfor %}
                <tr class="total-row">
                    <td class="bold">Total ETP by period</td>
                    <td class="text-center period-total" data-period="2025 Q1-Q2">
                        {{ "%.2f"|format(period_totals["2025 Q1-Q2"]) }}
                    </td>
                    <td class="text-center period-total" data-period="2025 Q3-Q4">
                        {{ "%.2f"|format(period_totals["2025 Q3-Q4"]) }}
                    </td>
                    <td class="text-center period-total" data-period="2026-2027">
                        {{ "%.2f"|format(period_totals["2026-2027"]) }}
                    </td>
                    <td class="text-center grand-total">{{ "%.2f"|format(total_max_etp) }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="{{ url_for('static', filename='js/project/etp_table.js') }}"></script>
{% endblock %}
```

### timeline.css
```css
/* Variables globales */
:root {
    --sidebar-width: 200px;
    --row-height: 3.5rem;
    --task-height: calc(100% - 1rem);
    --grid-columns: 5;
}

/* Reset du conteneur principal */
.main-content {
    max-width: 100%;
    margin: 0;
    padding: 0;
}

/* Conteneur de la timeline */
.timeline-container {
    background-color: white;
    padding: 1rem;
    width: 100%;
}

/* En-tête de la page */
.page-title {
    padding: 0 2rem;
    margin-bottom: 1rem;
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--primary-color);
}

/* Toggles des streams */
.stream-toggles {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 1rem;
    padding: 1rem 2rem;
    background-color: #f8fafc;
    border-radius: 0.5rem;
}

.stream-toggle {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
}

/* Style du switch */
.switch {
    position: relative;
    display: inline-block;
    width: 48px;
    height: 24px;
}

.switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider {
    position: absolute;
    cursor: pointer;
    inset: 0;
    background-color: #e5e7eb;
    transition: .3s;
    border-radius: 24px;
}

.slider:before {
    content: "";
    position: absolute;
    height: 18px;
    width: 18px;
    left: 3px;
    bottom: 3px;
    background-color: white;
    transition: .3s;
    border-radius: 50%;
}

input:checked + .slider {
    background-color: var(--primary-color);
}

input:checked + .slider:before {
    transform: translateX(24px);
}

/* Structure principale de la timeline */
.timeline-grid {
    width: 100%;
    overflow-x: auto;
}

.timeline-main {
    width: 100%;
    min-width: 100%;
    padding: 0 1rem;
}

.period {
    padding: 0.5rem;
    text-align: center;
    border-right: 1px solid rgba(255, 255, 255, 0.2);
    font-size: 0.875rem;
}

/* Grille des périodes */
.periods-grid {
    display: grid; 
    grid-template-columns: var(--sidebar-width) repeat(var(--grid-columns), 1fr);
    background-color: var(--primary-color);
    gap: 0;
    color: white;
    border-radius: 0.25rem;
    position: sticky;
    top: 0;
    z-index: 10;
}



/* Conteneur des lignes */
.timeline-rows-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 1rem;
}

/* Ligne de projet */
.timeline-row {
    display: grid;
    grid-template-columns: var(--sidebar-width) 1fr;
    min-height: var(--row-height);
    margin-bottom: 0.5rem;
}

/* Nom du projet */
.project-name {
    font-weight: 600;
    padding: 0.5rem 1rem;
    background-color: #f9fafb;
    border-radius: 0.25rem 0 0 0.25rem;
    display: flex;
    align-items: center;
}

/* Conteneur des tâches */
.project-tasks {
    position: relative;
    background-color: #f9fafb;
    border-radius: 0 0.25rem 0.25rem 0;
    padding: 0.5rem;
    min-height: var(--row-height);
    width: 100%;
}

/* Style des lignes de la grille */
.project-tasks::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image: linear-gradient(
        to right,
        rgba(0, 0, 0, 0.1) 1px,
        transparent 1px
    );
    background-size: calc(100% / var(--grid-columns)) 100%;
    pointer-events: none;
    z-index: 0;
}

/* Style des tâches */
.task {
    position: absolute;
    max-width: 100%; /* Cela pourrait limiter la largeur */
    height: var(--task-height);
    padding: 0.5rem;
    border-radius: 0.25rem;
    font-size: 0.75rem;
    color: white;
    cursor: pointer;
    display: flex;
    align-items: center;
    transition: transform 0.2s, box-shadow 0.2s;
    white-space: nowrap;
    text-overflow: ellipsis;
    z-index: 1;
}

.task:hover {
    transform: translateY(-2px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    z-index: 2;
}

.task:hover::after {
    content: attr(data-dates);
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: 0.25rem;
    font-size: 0.75rem;
    white-space: nowrap;
    z-index: 1000;
}

/* Styles des jalons */
.milestones {
    margin-top: 2rem;
}

.milestone-container {
    position: relative;
    height: 4rem;
    background-color: #f9fafb;
    border-radius: 0.25rem;
    padding: 1rem;
}

.milestone {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
}

.milestone-dot {
    width: 1rem;
    height: 1rem;
    background-color: var(--secondary-color);
    border-radius: 50%;
    margin: 0 auto;
}

.milestone-text {
    position: absolute;
    width: max-content;
    left: 50%;
    transform: translateX(-50%);
    margin-top: 0.5rem;
    font-size: 0.75rem;
    font-weight: 500;
}

/* Animation pour masquer/afficher les lignes */
.timeline-row {
    transition: all 0.3s ease;
}

.timeline-row.hidden {
    display: none;
}

/* Couleurs des tâches */
.task.bg-blue-600 { background-color: #2563eb; }
.task.bg-blue-500 { background-color: #3b82f6; }
.task.bg-blue-400 { background-color: #60a5fa; }

.task.bg-purple-600 { background-color: #9333ea; }
.task.bg-purple-500 { background-color: #a855f7; }
.task.bg-purple-400 { background-color: #c084fc; }

.task.bg-green-600 { background-color: #16a34a; }
.task.bg-green-500 { background-color: #22c55e; }
.task.bg-green-400 { background-color: #4ade80; }

.task.bg-yellow-600 { background-color: #ca8a04; }
.task.bg-yellow-500 { background-color: #eab308; }
.task.bg-yellow-400 { background-color: #facc15; }

.task.bg-red-600 { background-color: #dc2626; }
.task.bg-red-500 { background-color: #ef4444; }
.task.bg-red-400 { background-color: #f87171; }

.task.bg-indigo-600 { background-color: #4f46e5; }
.task.bg-indigo-500 { background-color: #6366f1; }
.task.bg-indigo-400 { background-color: #818cf8; }

.task.bg-teal-600 { background-color: #0d9488; }
.task.bg-teal-500 { background-color: #14b8a6; }
.task.bg-teal-400 { background-color: #2dd4bf; }

.task.bg-gray-600 { background-color: #4b5563; }
.task.bg-gray-500 { background-color: #6b7280; }
.task.bg-gray-400 { background-color: #9ca3af; }

/* Responsive */
@media (max-width: 1024px) {
    :root {
        --sidebar-width: 150px;
    }
    
    .project-name {
        font-size: 0.875rem;
    }
    
    .task {
        font-size: 0.75rem;
    }
}







/* Modal */

.modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5);
    z-index: 1000;
}

.modal-content {
    background-color: white;
    margin: 10% auto;
    padding: 20px;
    border-radius: 8px;
    width: 90%;
    max-width: 500px;
    position: relative;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.modal-header h2 {
    margin: 0;
    color: var(--primary-color);
}

.close {
    font-size: 24px;
    cursor: pointer;
    color: #666;
}

.form-group {
    margin-bottom: 15px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    color: #333;
}

.form-group input,
.form-group select {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.modal-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1.5rem;
}

.btn-primary, .btn-secondary, .btn-danger {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 0.25rem;
    cursor: pointer;
    font-size: 0.875rem;
    font-weight: 500;
    height: 38px;
}

.btn-primary {
    background-color: var(--primary-color);
    color: white;
}

.btn-secondary {
    background-color: #e5e7eb;
    color: #374151;
}

.action-buttons {
    display: flex;
    gap: 0.5rem;
}

/* Animations */
.modal.show {
    display: block;
    animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Style pour l'aperçu des couleurs */
.color-preview {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 8px;
    vertical-align: middle;
}


/* Modal edition */

.btn-danger {
    background-color: #dc2626;
    color: white;
}

.btn-danger:hover {
    background-color: #b91c1c;
}

/* Style pour le modal d'édition */
#editTaskModal .modal-content {
    max-width: 600px;
}

#editTaskModal .form-group {
    margin-bottom: 1rem;
}

#editTaskModal .modal-footer {
    display: flex;
    justify-content: space-between;
    margin-top: 1.5rem;
}

#editTaskModal .modal-footer .btn-danger {
    margin-right: auto;
}

/* Style pour le projet désactivé */
#editTaskProject:disabled {
    background-color: #f3f4f6;
    cursor: not-allowed;
}

.project-name {
    font-weight: 600;
    padding: 0.5rem 1rem;
    background-color: #f9fafb;
    border-radius: 0.25rem 0 0 0.25rem;
    display: flex;
    align-items: center;
    cursor: pointer;
    transition: all 0.2s ease;
}

.project-name:hover {
    background-color: var(--primary-color);
    color: white;
}
```

### normalize.css
```css
/* Modern CSS Reset */
*,
*::before,
*::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

/* Basic resets and defaults */
body {
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
}

img,
picture,
video,
canvas,
svg {
    display: block;
    max-width: 100%;
}

input,
button,
textarea,
select {
    font: inherit;
}

p,
h1,
h2,
h3,
h4,
h5,
h6 {
    overflow-wrap: break-word;
}
```

### etp_table.css
```css
.etp-container {
    background-color: white;
    border-radius: 0.5rem;
    padding: 2rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.etp-table-container {
    overflow-x: auto;
}

.etp-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
}

.etp-table th,
.etp-table td {
    padding: 0.75rem 1rem;
    border: 1px solid var(--border-color);
}

.etp-table th {
    background-color: var(--primary-color);
    color: white;
    font-weight: 500;
    text-align: left;
}

.etp-table td {
    background-color: white;
}

.text-center {
    text-align: center;
}

.bold {
    font-weight: 600;
}

.total-row {
    background-color: #f8fafc;
}

.total-row td {
    background-color: #f8fafc;
}

.editable-cell {
    cursor: pointer;
    position: relative;
    transition: background-color 0.2s;
}

.editable-cell:hover {
    background-color: #f0f9ff;
}

.editable-cell .etp-value {
    display: block;
    width: 100%;
    height: 100%;
}

.editable-cell input {
    width: 100%;
    height: 100%;
    padding: 0.75rem 1rem;
    border: 2px solid var(--primary-color);
    text-align: center;
    font-size: inherit;
    background-color: white;
    position: absolute;
    top: 0;
    left: 0;
    margin: 0;
    box-sizing: border-box;
}

.editable-cell input:focus {
    outline: none;
    border: 2px solid var(--secondary-color);
}

/* Animation pour les mises à jour */
.updated {
    animation: highlight 1s ease-out;
}

@keyframes highlight {
    0% {
        background-color: #93c5fd;
    }
    100% {
        background-color: transparent;
    }
}

/* Style spécifique pour les totaux */
.row-total,
.period-total,
.grand-total {
    font-weight: 600;
    background-color: #f8fafc;
}
```

### base.css
```css
:root {
    --primary-color: #312e81;
    --secondary-color: #3b82f6;
    --background-color: #f3f4f6;
    --text-color: #1f2937;
    --border-color: #e5e7eb;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
    background-color: var(--background-color);
    color: var(--text-color);
}

.main-nav {
    background-color: var(--primary-color);
    padding: 1rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-content {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    color: white;
    text-decoration: none;
    font-weight: bold;
    font-size: 1.25rem;
}

.nav-links {
    list-style: none;
    display: flex;
    gap: 2rem;
}

.nav-links a {
    color: white;
    text-decoration: none;
    padding: 0.5rem 1rem;
    border-radius: 0.25rem;
    transition: background-color 0.3s;
}

.nav-links a:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

.main-content {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 1rem;
}

.main-footer {
    background-color: var(--primary-color);
    color: white;
    text-align: center;
    padding: 1rem;
    position: fixed;
    bottom: 0;
    width: 100%;
}

.page-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 2rem;
    color: var(--primary-color);
}




```

### config.py
```py
from datetime import timedelta

class Config:
    SECRET_KEY = 'your-secret-key-here'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///project_manager.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
```

### run.py
```py
from app import create_app, db
from app.services.init_data import init_db_data
import logging
import os

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()

# Nom du fichier de la base de données
DB_FILE = 'instance/project_manager.db'

if __name__ == '__main__':
    with app.app_context():
        try:
            # Vérifie si la base de données existe déjà
            db_exists = os.path.exists(DB_FILE)
            
            if not db_exists:
                logger.info("Base de données non trouvée, création initiale...")
                db.create_all()
                logger.info("Tables créées avec succès")
                
                logger.info("Initialisation avec les données de test...")
                init_db_data()
                logger.info("Données de test initialisées avec succès")
            else:
                logger.info("Base de données existante trouvée, conservation des données...")
        
        except Exception as e:
            logger.error(f"Une erreur est survenue : {str(e)}")
            raise e
        
    logger.info("Démarrage de l'application Flask...")
    app.run(debug=True)
```

### __init__.py
```py
from .main import bp as main
from .project import bp as project

__all__ = ['main', 'project']
```

### project.py
```py
from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from app.services import ProjectService, EtpService
from app.models import Project, Task
from app.constants import TimeConstants
from datetime import datetime
from app import db

bp = Blueprint('project', __name__, url_prefix='/project')

# Utilitaires communs
def make_response(data=None, error=None, status=200):
    """Utilitaire pour standardiser les réponses API"""
    if error:
        return jsonify({'error': str(error)}), status
    return jsonify({'status': 'success', 'data': data}), status

# Routes de pages (Views)
@bp.route('/timeline')
def timeline():
    """Page de la timeline des projets"""
    projects = ProjectService.get_all_projects()
    return render_template('project/timeline.html',
                         projects=[p.to_dict() for p in projects],
                         periods=TimeConstants.PERIODS_DISPLAY,
                         milestones=TimeConstants.MILESTONES)

@bp.route('/etp')
def etp_redirect():
    """Redirection vers la table ETP"""
    return redirect(url_for('project.etp_table'))

@bp.route('/etp_table')
def etp_table():
    """Page de la table ETP"""
    projects = ProjectService.get_all_projects()
    etp_data, period_totals = EtpService.calculate_etp_per_period(projects)
    total_max_etp = sum(row["total"] for row in etp_data)
    return render_template('project/etp_table.html',
                         etp_data=etp_data,
                         period_totals=period_totals,
                         total_max_etp=total_max_etp)

# API Routes - Projects
@bp.route('/api/projects', methods=['GET'])
def get_projects():
    """Liste tous les projets"""
    try:
        projects = ProjectService.get_all_projects()
        return make_response(data={'projects': [{'id': p.id, 'name': p.name} for p in projects]})
    except Exception as e:
        return make_response(error=e, status=500)

@bp.route('/api/projects', methods=['POST'])
def create_project():
    """Crée un nouveau projet"""
    try:
        data = request.json
        name = data.get('name')
        if not name:
            return make_response(error='Le nom du projet est requis', status=400)
            
        color_scheme = data.get('colorScheme', 'blue')
        project = ProjectService.create_project(name, color_scheme)
        
        return make_response(
            data={'project': {'id': project.id, 'name': project.name}},
            status=201
        )
    except ValueError as e:
        return make_response(error=e, status=400)
    except Exception as e:
        return make_response(error='Erreur lors de la création du projet', status=500)

@bp.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """Met à jour un projet existant"""
    try:
        data = request.json
        project = Project.query.get(project_id)
        
        if not project:
            return make_response(error='Projet non trouvé', status=404)
            
        # Mise à jour uniquement des champs fournis
        if 'name' in data:
            project.name = data['name']
        if 'colorScheme' in data:
            project.color_scheme = data['colorScheme']
        
        db.session.commit()
        
        return make_response(data={
            'project': project.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return make_response(error=str(e), status=500)

@bp.route('/api/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Supprime un projet et ses tâches associées"""
    try:
        success = ProjectService.delete_project(project_id)
        if not success:
            return make_response(error='Projet non trouvé', status=404)
        return make_response()
    except Exception as e:
        db.session.rollback()
        return make_response(error=e, status=500)

# API Routes - Tasks
@bp.route('/api/tasks', methods=['POST'])
def create_task():
    """Crée une nouvelle tâche"""
    try:
        data = request.json
        required_fields = ['project_id', 'text', 'start_date', 'end_date']
        
        if not all(field in data for field in required_fields):
            return make_response(error='Tous les champs requis doivent être renseignés', status=400)
        
        # Traitement des dates et création de la tâche
        task = ProjectService.create_task(
            project_id=int(data['project_id']),
            text=data['text'],
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
            color=None,  # La couleur sera déterminée par le service
            etp=float(data.get('etp', 1.0))
        )
        
        if not task:
            return make_response(error="La tâche n'a pas été créée correctement", status=500)
            
        return make_response(data={'task': task.to_dict()}, status=201)
        
    except Exception as e:
        return make_response(error=e, status=500)

@bp.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Met à jour une tâche existante"""
    try:
        data = request.json
        task = Task.query.get(task_id)
        
        if not task:
            return make_response(error='Tâche non trouvée', status=404)
            
        # Mise à jour des champs
        task.text = data.get('text', task.text)
        task.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        task.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        task.etp = float(data.get('etp', task.etp))
        
        db.session.commit()
        
        return make_response(data={'task': task.to_dict()})
        
    except Exception as e:
        db.session.rollback()
        return make_response(error=e, status=500)

@bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Supprime une tâche"""
    try:
        success = ProjectService.delete_task(task_id)
        if not success:
            return make_response(error='Tâche non trouvée', status=404)
        return make_response()
    except Exception as e:
        return make_response(error=e, status=500)
```

### main.py
```py
from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('base.html')
```

### etp_entry.py
```py
from app import db
from datetime import datetime

class EtpEntry(db.Model):
    __tablename__ = 'etp_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    period = db.Column(db.String(20), nullable=False)
    etp_value = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('project_id', 'period', name='uix_project_period'),
    )

```

### project.py
```py
from app import db
from datetime import datetime

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    color_scheme = db.Column(db.String(50), nullable=False, default='blue')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    tasks = db.relationship('Task', backref='project', lazy=True, cascade='all, delete-orphan')
    etp_entries = db.relationship('EtpEntry', backref='project', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'color_scheme': self.color_scheme,
            'tasks': [task.to_dict() for task in self.tasks]
        }
```

### __init__.py
```py
from .project import Project
from .task import Task
from .etp_entry import EtpEntry

__all__ = ['Project', 'Task', 'EtpEntry']
```

### env.py
```py
import logging
from logging.config import fileConfig

from flask import current_app

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')


def get_engine():
    try:
        # this works with Flask-SQLAlchemy<3 and Alchemical
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        # this works with Flask-SQLAlchemy>=3
        return current_app.extensions['migrate'].db.engine


def get_engine_url():
    try:
        return get_engine().url.render_as_string(hide_password=False).replace(
            '%', '%%')
    except AttributeError:
        return str(get_engine().url).replace('%', '%%')


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
config.set_main_option('sqlalchemy.url', get_engine_url())
target_db = current_app.extensions['migrate'].db

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_metadata():
    if hasattr(target_db, 'metadatas'):
        return target_db.metadatas[None]
    return target_db.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=get_metadata(), literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # this callback is used to prevent an auto-migration from being generated
    # when there are no changes to the schema
    # reference: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    conf_args = current_app.extensions['migrate'].configure_args
    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            **conf_args
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

```

### task.py
```py
from app import db
from datetime import datetime, date

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    color = db.Column(db.String(50), nullable=False)
    etp = db.Column(db.Float, default=1.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def _calculate_grid_position(self):
        """Calcule la position relative dans la grille."""
        def get_quarter_position(d: date) -> float:
            if d.year > 2025:
                return 80.0
            
            quarter = (d.month - 1) // 3
            base_position = quarter * 20.0
            
            month_in_quarter = (d.month - 1) % 3
            days_in_quarter = 90
            days_from_quarter_start = (month_in_quarter * 30) + (d.day - 1)
            relative_position = (days_from_quarter_start / days_in_quarter) * 20.0
            
            return base_position + relative_position
        
        start_pos = get_quarter_position(self.start_date)
        end_pos = get_quarter_position(self.end_date)
        
        if end_pos < start_pos:
            end_pos = 100.0
        
        width = end_pos - start_pos
        
        if width < 15 and (self.end_date.month - self.start_date.month >= 1):
            width = 15
        elif width < 8:
            width = 8
        
        return start_pos, width
    
    def to_dict(self):
        start, width = self._calculate_grid_position()
        return {
            'id': self.id,
            'project_id': self.project_id,
            'text': self.text,
            'start_date': self.start_date.strftime('%d/%m/%Y'),  # Format de date pour l'affichage
            'end_date': self.end_date.strftime('%d/%m/%Y'),      # Format de date pour l'affichage
            'dates': f"{self.start_date.strftime('%d/%m/%Y')} - {self.end_date.strftime('%d/%m/%Y')}", # Pour l'infobulle
            'raw_start_date': self.start_date.isoformat(),  # Pour l'édition
            'raw_end_date': self.end_date.isoformat(),      # Pour l'édition
            'color': self.color,
            'etp': self.etp,
            'start': start,
            'width': width
        }

```

