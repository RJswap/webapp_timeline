### run.py
```py
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
```

### config.py
```py
class Config:
    SECRET_KEY = 'your-secret-key-here'
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
```

### __init__.py
```py
from flask import Flask
from config import DevelopmentConfig

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Register blueprints
    from app.routes import main, project
    app.register_blueprint(main.bp)
    app.register_blueprint(project.bp)
    
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

### timeline.css
```css
.timeline-container {
    background-color: white;
    border-radius: 0.5rem;
    padding: 2rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.periods-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    background-color: var(--primary-color);
    color: white;
    border-radius: 0.25rem;
    overflow: hidden;
}

.period {
    padding: 0.5rem;
    text-align: center;
    border-right: 1px solid rgba(255, 255, 255, 0.2);
    font-size: 0.875rem;
}

.project-row {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
    padding: 0.5rem;
    border-radius: 0.25rem;
    background-color: #f9fafb;
}

.project-name {
    font-weight: 600;
    width: 8rem;
    padding-right: 1rem;
}

.project-tasks {
    flex-grow: 1;
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 0.25rem;
}

.task {
    padding: 0.5rem;
    border-radius: 0.25rem;
    font-size: 0.75rem;
    color: white;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.task:hover {
    transform: translateY(-2px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    overflow: visible;
    white-space: normal;
    z-index: 1;
}

/* Milestones styles */
.milestones {
    margin-top: 3rem;
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
}

/* Specific milestone positions */
.milestone.left-1\/3 {
    left: 33.33%;
}

.milestone.left-1\/2 {
    left: 50%;
}

.milestone.left-2\/3 {
    left: 66.66%;
}

.milestone.right-1\/6 {
    left: 83.33%;
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
    font-size: 0.75rem;
    text-align: center;
    margin-top: 0.5rem;
    font-weight: 500;
    transform: translateX(-50%);
    white-space: nowrap;
}

/* Task colors */
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

/* Responsive adjustments */
@media (max-width: 768px) {
    .project-name {
        width: 6rem;
    }
    
    .task {
        font-size: 0.7rem;
    }
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

### etp_table.js
```js
// static/js/project/etp_table.js

document.addEventListener('DOMContentLoaded', function() {
    const table = document.querySelector('.etp-table');
    let activeInput = null;

    // Gérer le clic sur une cellule éditable
    document.addEventListener('click', function(e) {
        // Vérifier si on clique sur une cellule éditable ou son contenu
        const cell = e.target.closest('.editable-cell');
        if (!cell) return; // Si on n'a pas cliqué sur une cellule éditable
        if (cell.querySelector('input')) return; // Si la cellule est déjà en mode édition

        // Récupérer la valeur actuelle
        const valueSpan = cell.querySelector('.etp-value');
        const currentValue = valueSpan.textContent.trim();

        // Créer l'input
        const input = document.createElement('input');
        input.type = 'number';
        input.step = '0.1';
        input.min = '0';
        input.value = currentValue;
        input.className = 'etp-input';

        // Cacher la valeur et ajouter l'input
        valueSpan.style.display = 'none';
        cell.appendChild(input);
        input.focus();
        activeInput = input;

        // Sélectionner tout le texte
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

            // Mettre à jour l'affichage
            const valueSpan = cell.querySelector('.etp-value');
            valueSpan.textContent = parseFloat(newValue).toFixed(2);
            valueSpan.style.display = '';
            valueSpan.classList.add('updated');
            
            // Supprimer l'input
            if (cell.querySelector('input')) {
                cell.querySelector('input').remove();
            }

            // Mettre à jour les totaux
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
        const periods = ['2024 Q3-Q4', '2025 Q1-Q2', '2025 Q3-Q4', '2026-2027'];
        
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

### project_service.py
```py
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
```

### etp_service.py
```py
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

    <footer class="main-footer">
        <p>&copy; 2025 Project Manager</p>
    </footer>

    <script src="{{ url_for('static', filename='js/base.js') }}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>

```

### constants.py
```py
class TimeConstants:
    PERIODS_MAPPING = {
        1: "2024 Q3-Q4",
        2: "2025 Q1-Q2",
        3: "2025 Q3-Q4",
        4: "2026-2027"
    }
    
    PERIODS_DISPLAY = [
        "2024 Q3-Q4",
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

### task.py
```py
from dataclasses import dataclass
import re
from typing import Optional

@dataclass
class Task:
    start: int
    width: int
    color: str
    text: str
    etp: Optional[float] = None
    
    def __post_init__(self):
        if self.etp is None:
            self.etp = self._extract_etp_from_text()
    
    def _extract_etp_from_text(self) -> float:
        """Extrait la valeur ETP du texte de manière plus robuste."""
        # Pattern pour trouver les valeurs ETP comme (1 ETP) ou (0.5 ETP) ou (1.5 ETP)
        etp_pattern = r'\((\d*\.?\d+)\s*ETP\)'
        match = re.search(etp_pattern, self.text)
        
        if match:
            try:
                return float(match.group(1))
            except (ValueError, IndexError):
                return 0.0
        return 0.0
    
    def to_dict(self):
        return {
            'start': self.start,
            'width': self.width,
            'color': self.color,
            'text': self.text,
            'etp': self.etp
        }
```

### project.py
```py
from flask import Blueprint, render_template
from flask import jsonify, request
from app.services.project_service import ProjectService
from app.services.etp_service import EtpService
from app.constants import TimeConstants

bp = Blueprint('project', __name__, url_prefix='/project')

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


from flask import redirect, url_for

@bp.route('/etp')
def etp_redirect():
    return redirect(url_for('project.etp_table'))

from flask import jsonify, request

@bp.route('/api/update_etp', methods=['POST'])
def update_etp():
    try:
        data = request.json
        project_name = data.get('project')
        period = data.get('period')
        new_etp = float(data.get('etp'))
        
        # Pour l'instant, nous ne persistons pas les données
        # Vous pourriez ajouter ici la logique de sauvegarde en base de données
        
        return jsonify({
            'status': 'success',
            'message': f'ETP updated for {project_name} in period {period}'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
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

### main.py
```py
from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('base.html')
```

### timeline.html
```html
{% extends "base.html" %}

{% block title %}Timeline - Project Manager{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/project/timeline.css') }}">
{% endblock %}

{% block content %}
<div class="timeline-container">
    <h1 class="page-title">Project Timeline</h1>
    
    <!-- Header avec les périodes -->
    <div class="header-container">
        <div class="periods-grid">
            {% for period in periods %}
            <div class="period">{{ period }}</div>
            {% endfor %}
        </div>
    </div>

    <!-- Contenu de la timeline -->
    <div class="timeline-content">
        {% for project in projects %}
        <div class="project-row">
            <div class="project-name">{{ project.name }}</div>
            <div class="project-tasks">
                {% for task in project.tasks %}
                <div class="task bg-{{ task.color }}"
                     style="grid-column: {{ task.start }} / span {{ task.width }};"
                     data-task-info="{{ task.text }}">
                    {{ task.text }}
                </div>
                {% endfor %}
            </div>
        </div>
        {% endfor %}

        <!-- Jalons clés -->
        <div class="milestones">
            <div class="project-name">Jalons clés</div>
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
                    <th>2024 Q3-Q4</th>
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
                    <td class="text-center editable-cell" data-period="2024 Q3-Q4">
                        <span class="etp-value">{{ "%.2f"|format(row["2024 Q3-Q4"]) }}</span>
                    </td>
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
                    <td class="text-center period-total" data-period="2024 Q3-Q4">
                        {{ "%.2f"|format(period_totals["2024 Q3-Q4"]) }}
                    </td>
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

