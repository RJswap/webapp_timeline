### run.py
```py
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
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

### project.py
```py
from flask import Blueprint, render_template
from flask import jsonify, request
from flask import redirect, url_for
from app.services.project_service import ProjectService
from app.services.etp_service import EtpService
from app.constants import TimeConstants

bp = Blueprint('project', __name__, url_prefix='/project')



@bp.route('/etp')
def etp_redirect():
    return redirect(url_for('project.etp_table'))


@bp.route('/timeline')
def timeline():
    projects = ProjectService.get_all_projects()
    return render_template('project/timeline.html', 
                         projects=[p.to_dict() for p in projects], 
                         periods=TimeConstants.PERIODS_DISPLAY, 
                         milestones=TimeConstants.MILESTONES)

@bp.route('/etp_table')
def etp_table():
    projects = ProjectService.get_all_projects()
    etp_data, period_totals = EtpService.calculate_etp_per_period(projects)
    total_max_etp = sum(row["total"] for row in etp_data)
    
    return render_template('project/etp_table.html', 
                         etp_data=etp_data, 
                         period_totals=period_totals,
                         total_max_etp=total_max_etp)



@bp.route('/api/update_etp', methods=['POST'])
def update_etp():
    try:
        # Validate request data
        if not request.is_json:
            return jsonify({
                'status': 'error',
                'message': 'Request must be JSON'
            }), 400

        data = request.json
        project_name = data.get('project')
        period = data.get('period')
        etp_str = data.get('etp')

        # Validate required fields
        if not all([project_name, period, etp_str]):
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields: project, period, and etp'
            }), 400

        # Convert and validate ETP value
        try:
            new_etp = float(etp_str)
            if new_etp < 0:
                raise ValueError("ETP value cannot be negative")
        except ValueError as e:
            return jsonify({
                'status': 'error',
                'message': f'Invalid ETP value: {str(e)}'
            }), 400
        
        # Update ETP in database
        EtpService.update_etp(project_name, period, new_etp)
        
        return jsonify({
            'status': 'success',
            'message': f'ETP updated for {project_name} in period {period}',
            'data': {
                'project': project_name,
                'period': period,
                'etp': new_etp
            }
        })

    except Exception as e:
        app.logger.error(f"Error updating ETP: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to update ETP: {str(e)}'
        }), 500
```

### main.py
```py
from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('base.html')
```

### __init__.py
```py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import DevelopmentConfig

db = SQLAlchemy()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    from app.routes import main, project
    app.register_blueprint(main.bp)
    app.register_blueprint(project.bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
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
    window.onerror = function(msg, url, lineNo, columnNo, error) {
        console.error('Error: ', msg, url, lineNo, columnNo, error);
        notifications.show('Une erreur est survenue', 'error');
        return false;
    };

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

### project_service.py
```py
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
                    Task(start_date=date(2025,3,1), end_date=date(2025, 4, 30), color="blue-600", text="Analyse contrats & RFI"),
                    Task(start_date=date(2025,4,30), end_date=date(2025, 7, 30), color="blue-500", text="RFP & Négociations")
                ]
            ),
             Project(
                name="Workforce & HR",
                tasks=[
                    Task(start_date=date(2025,2,1), end_date=date(2025, 4, 30), color="purple-600", text="Initiation"),
                    Task(start_date=date(2025,5,1), end_date=date(2025, 6, 30), color="purple-500", text="Analyse & Design"),
                    Task(start_date=date(2025,7,1), end_date=date(2025, 8, 30), color="purple-400", text="Accompagnement & Déploiement")
                ]
            ),
            Project(
                name="EUS",
                tasks=[
                    Task(start_date=date(2025,2,1), end_date=date(2025, 4, 30), color="green-600", text="Due Diligence"),
                    Task(start_date=date(2025,5,1), end_date=date(2025, 6, 30), color="green-500", text="RFP (3 ETP)"),
                    Task(start_date=date(2025,7,1), end_date=date(2025, 8, 30), color="green-400", text="Pilot & Deploy")
                ]
            ),
            Project(
                name="VIP/Events",
                tasks=[
                    Task(start_date=date(2025,2,1), end_date=date(2025, 4, 30), color="yellow-600", text="Analyse & Design")
                ]
            ),
            Project(
                name="Employee Experience",
                tasks=[
                    Task(start_date=date(2025,2,1), end_date=date(2025, 4, 30), color="red-600", text="Benchmark & Design"),
                    Task(start_date=date(2025,5,1), end_date=date(2025, 6, 30), color="red-500", text="Implementation & Optimization")
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
```

### etp_service.py
```py
from collections import defaultdict
from typing import List, Dict, Tuple
from datetime import date
from app.models.project import Project
from app.models.etp_entry import EtpEntry
from app.constants import TimeConstants
from datetime import datetime
from app import db

class EtpService:
    @staticmethod
    def get_stored_etp(project_name: str, period: str) -> float:
        """Récupère la valeur ETP stockée pour un projet et une période donnés"""
        entry = EtpEntry.query.filter_by(
            project_name=project_name,
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
    def get_task_etp_by_date(project_name: str, task_date: date, default_etp: float) -> float:
        """Récupère l'ETP pour une tâche à une date spécifique"""
        period = EtpService.get_period_for_date(task_date)
        stored_etp = EtpService.get_stored_etp(project_name, period)
        return stored_etp if stored_etp is not None else default_etp

    @staticmethod
    def calculate_etp_per_period(projects: List[Project]) -> Tuple[List[Dict], Dict[str, float]]:
        etp_data = []
        period_totals = defaultdict(float)
        
        for project in projects:
            project_etps = defaultdict(float)
            max_etp = 0
            
            stored_etps = EtpEntry.query.filter_by(project_name=project.name).all()
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
    def update_etp(project_name: str, period: str, etp_value: float) -> None:
        """Update ETP value in database"""
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
                etp_value=etp_value
            )
            db.session.add(entry)
            
        db.session.commit()
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
    <link rel="stylesheet" href="{{ url_for('static', filename='css/timeline.css') }}">
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
                    <div class="timeline-row" data-project-name="{{ project.name }}">
                        <div class="project-name">{{ project.name }}</div>
                        <div class="project-tasks">
                            {% for task in project.tasks %}
                            {% set start_percent = (task.start - 1) * (100/6) %}
                            {% set width_percent = task.width * (100/6) %}
                            <div class="task bg-{{ task.color }}"
                                style="left: {{ start_percent }}%; width: {{ width_percent }}%;"
                                data-task-info="{{ task.text }}"
                                data-dates="{{ task.start_date }} - {{ task.end_date }}">
                                {{ task.text }}
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                    {% endfor %}
                </div>

                <!-- Jalons clés -->
                <div class="milestones">
                    <div class="milestone-container">
                        {% for milestone in milestones %}
                        <div class="milestone {{ milestone.position }}">
                            <div class="milestone-dot"></div>
                            <div class="milestone-text">{{ milestone.text }}</div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
    </div>
{% endblock %}

{% block extra_js %}
<script src="{{ url_for('static', filename='js/project/timeline.js') }}"></script>
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

.period {
    padding: 0.5rem;
    text-align: center;
    border-right: 1px solid rgba(255, 255, 255, 0.2);
    font-size: 0.875rem;
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
    overflow: hidden;
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
    max-width: 100%;
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
    overflow: hidden;
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
.bg-blue-600 { background-color: #2563eb; }
.bg-blue-500 { background-color: #3b82f6; }
.bg-purple-600 { background-color: #9333ea; }
.bg-purple-500 { background-color: #a855f7; }
.bg-purple-400 { background-color: #c084fc; }
.bg-green-600 { background-color: #16a34a; }
.bg-green-500 { background-color: #22c55e; }
.bg-green-400 { background-color: #4ade80; }
.bg-yellow-600 { background-color: #ca8a04; }
.bg-red-600 { background-color: #dc2626; }
.bg-red-500 { background-color: #ef4444; }
.bg-indigo-600 { background-color: #4f46e5; }
.bg-indigo-500 { background-color: #6366f1; }
.bg-teal-600 { background-color: #0d9488; }
.bg-teal-500 { background-color: #14b8a6; }
.bg-gray-600 { background-color: #4b5563; }
.bg-gray-500 { background-color: #6b7280; }

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
                    <td class="bold">Total ETP par période</td>
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

### task.py
```py
from dataclasses import dataclass
import re
from typing import Optional
from datetime import date, datetime

@dataclass
class Task:
    start_date: date
    end_date: date
    color: str
    text: str
    etp: Optional[float] = None
    
    def __post_init__(self):
        if self.etp is None:
            self.etp = self._extract_etp_from_text()
    
    def _extract_etp_from_text(self) -> float:
        etp_pattern = r'\((\d*\.?\d+)\s*ETP\)'
        match = re.search(etp_pattern, self.text)
        return float(match.group(1)) if match else 0.0
    
    def _calculate_grid_position(self) -> tuple[float, float]:
        """Calcule la position relative dans la grille.
        La grille est divisée en 5 colonnes égales de 20% chacune:
        - 2025 Q1: 0-20%
        - 2025 Q2: 20-40%
        - 2025 Q3: 40-60%
        - 2025 Q4: 60-80%
        - 2026-2027: 80-100%
        """
        def get_quarter_position(d: date) -> float:
            if d.year > 2025:
                return 80.0
            
            quarter = (d.month - 1) // 3  # 0-3 pour Q1-Q4
            base_position = quarter * 20.0  # Position de début du trimestre
            
            # Position relative dans le trimestre (0-20%)
            month_in_quarter = (d.month - 1) % 3
            days_in_quarter = 90  # Approximation pour un calcul plus simple
            days_from_quarter_start = (month_in_quarter * 30) + (d.day - 1)
            relative_position = (days_from_quarter_start / days_in_quarter) * 20.0
            
            return base_position + relative_position
        
        start_pos = get_quarter_position(self.start_date)
        end_pos = get_quarter_position(self.end_date)
        
        # Ajuster la largeur pour les tâches qui traversent les trimestres
        if end_pos < start_pos:  # Si la tâche se termine en 2026-2027
            end_pos = 100.0
        
        # Calculer la largeur
        width = end_pos - start_pos
        
        # Ajuster la largeur minimale pour la visibilité
        if width < 15 and (self.end_date.month - self.start_date.month >= 1):
            width = 15  # Largeur minimum pour les tâches de 2 mois ou plus
        elif width < 8:
            width = 8  # Largeur minimum pour les tâches courtes
        
        # Pour débogage
        print(f"Task: {self.text}")
        print(f"Dates: {self.start_date} -> {self.end_date}")
        print(f"Position: {start_pos:.1f}% -> {end_pos:.1f}%")
        print(f"Width: {width:.1f}%")
        print("---")
        
        return start_pos, width
    
    def to_dict(self):
        start, width = self._calculate_grid_position()
        return {
            'start': start,
            'width': width,
            'color': self.color,
            'text': self.text,
            'etp': self.etp,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat()
        }
```

### project.py
```py
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
```

### etp_entry.py
```py
from app import db
from datetime import datetime

class EtpEntry(db.Model):
    __tablename__ = 'etp_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    period = db.Column(db.String(20), nullable=False)
    etp_value = db.Column(db.Float, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('project_name', 'period', name='uix_project_period'),
    )

```

### timeline.js
```js
// static/js/project/timeline.js

document.addEventListener('DOMContentLoaded', function() {
    const timelineRows = document.querySelectorAll('.timeline-row');
    
    // Créer la barre de toggles
    const streamToggles = document.createElement('div');
    streamToggles.className = 'stream-toggles';
    
    // Créer un toggle pour chaque projet
    timelineRows.forEach((row) => {
        const projectName = row.dataset.projectName;
        const toggleWrapper = document.createElement('div');
        toggleWrapper.className = 'stream-toggle';
        
        // Créer le switch
        const label = document.createElement('label');
        label.className = 'switch';
        
        const input = document.createElement('input');
        input.type = 'checkbox';
        input.checked = true;
        
        const slider = document.createElement('span');
        slider.className = 'slider';
        
        label.appendChild(input);
        label.appendChild(slider);
        
        // Ajouter le label du projet
        const nameLabel = document.createElement('span');
        nameLabel.textContent = projectName;
        
        toggleWrapper.appendChild(label);
        toggleWrapper.appendChild(nameLabel);
        streamToggles.appendChild(toggleWrapper);
        
        // Gestionnaire d'événements pour le toggle
        input.addEventListener('change', function() {
            const isVisible = this.checked;
            toggleRowVisibility(row, isVisible);
            updatePositions();
        });
    });
    
    // Insérer la barre de toggles avant la timeline
    const timelineContainer = document.querySelector('.timeline-container');
    timelineContainer.insertBefore(streamToggles, timelineContainer.querySelector('.timeline-grid'));
    
    function toggleRowVisibility(row, isVisible) {
        if (isVisible) {
            row.classList.remove('hidden');
            row.style.height = '';
            row.style.opacity = '1';
        } else {
            row.classList.add('hidden');
            row.style.height = '0';
            row.style.opacity = '0';
        }
    }
    
    function updatePositions() {
        let currentOffset = 0;
        timelineRows.forEach(row => {
            if (!row.classList.contains('hidden')) {
                currentOffset += row.offsetHeight + 16; // 16px pour le gap
            }
        });
    }

    document.querySelectorAll('.task').forEach(task => {
        const left = task.style.left;
        const width = task.style.width;
        
        console.log(`Task: ${task.textContent.trim()}`);
        console.log(`Position CSS - left: ${left}, width: ${width}`);
        console.log(`Container width: ${task.parentElement.offsetWidth}px`);
        console.log('---');
        
        // Valider visuellement les positions
        task.title = `Position: ${left} | Width: ${width}`;
    });
});
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

