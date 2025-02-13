### app.py
```py
# app.py
from flask import Flask, render_template
from collections import defaultdict

app = Flask(__name__)

def calculate_etp_per_period(projects):
    etp_data = []
    period_totals = defaultdict(float)
    
    for project in projects:
        project_etps = defaultdict(float)
        max_etp = 0
        
        # Extraire le nombre d'ETP de chaque tâche
        for task in project["tasks"]:
            etp_value = float(task["text"].split("(")[-1].split(" ETP")[0])
            start_period = (task["start"] + 1) // 2  # Convertir en périodes semestrielles
            width_periods = (task["width"] + 1) // 2
            max_etp = max(max_etp, etp_value)
            
            # Répartir l'ETP sur les périodes concernées
            for period in range(start_period, start_period + width_periods):
                project_etps[period] = max(project_etps[period], etp_value)
        
        # Créer une ligne de données pour le projet
        project_row = {
            "name": project["name"],
            "2024 Q3-Q4": project_etps[1],
            "2025 Q1-Q2": project_etps[2],
            "2025 Q3-Q4": project_etps[3],
            "2026-2027": project_etps[4],
            "total": max_etp
        }
        
        # Mettre à jour les totaux par période
        for period, value in project_etps.items():
            period_name = {
                1: "2024 Q3-Q4",
                2: "2025 Q1-Q2",
                3: "2025 Q3-Q4",
                4: "2026-2027"
            }.get(period)
            if period_name:
                period_totals[period_name] += value
        
        etp_data.append(project_row)
    
    return etp_data, period_totals

@app.route('/')
def timeline():
    # Structure des données pour la timeline
    projects = [
        {
            "name": "Procurement",
            "tasks": [
                {"start": 2, "width": 2, "color": "blue-600", "text": "Analyse contrats & RFI (1 ETP)"},
                {"start": 4, "width": 2, "color": "blue-500", "text": "RFP & Négociations (1 ETP)"}
            ]
        },
        {
            "name": "Workforce & HR",
            "tasks": [
                {"start": 1, "width": 1, "color": "purple-600", "text": "Initiation (1 ETP)"},
                {"start": 2, "width": 2, "color": "purple-500", "text": "Analyse & Design (2 ETP)"},
                {"start": 4, "width": 3, "color": "purple-400", "text": "Accompagnement & Déploiement (2 ETP)"}
            ]
        },
        {
            "name": "EUS",
            "tasks": [
                {"start": 2, "width": 2, "color": "green-600", "text": "Due Diligence (3 ETP)"},
                {"start": 4, "width": 1, "color": "green-500", "text": "RFP (3 ETP)"},
                {"start": 5, "width": 2, "color": "green-400", "text": "Pilot & Deploy (3 ETP)"}
            ]
        },
        {
            "name": "VIP/Events",
            "tasks": [
                {"start": 1, "width": 2, "color": "yellow-600", "text": "Analyse & Design (0.5 ETP)"}
            ]
        },
        {
            "name": "Employee Experience",
            "tasks": [
                {"start": 2, "width": 2, "color": "red-600", "text": "Benchmark & Design (2 ETP)"},
                {"start": 4, "width": 3, "color": "red-500", "text": "Implementation & Optimization (2 ETP)"}
            ]
        },
        {
            "name": "Process Data Analytics",
            "tasks": [
                {"start": 2, "width": 2, "color": "indigo-600", "text": "Audit & Roadmap (3 ETP)"},
                {"start": 4, "width": 3, "color": "indigo-500", "text": "Implementation & Migration (3 ETP)"}
            ]
        },
        {
            "name": "Observability",
            "tasks": [
                {"start": 2, "width": 2, "color": "teal-600", "text": "Strategy & Design (2 ETP)"},
                {"start": 4, "width": 3, "color": "teal-500", "text": "POC & Implementation (2 ETP)"}
            ]
        },
        {
            "name": "TOM",
            "tasks": [
                {"start": 2, "width": 2, "color": "gray-600", "text": "Analysis & Design (2 ETP)"},
                {"start": 4, "width": 3, "color": "gray-500", "text": "Implementation & Transition (2 ETP)"}
            ]
        }
    ]

    periods = [
        "2024 Q3-Q4",
        "2025 Q1",
        "2025 Q2",
        "2025 Q3",
        "2025 Q4",
        "2026-2027"
    ]

    milestones = [
        {"position": "left-1/3", "text": "RFI"},
        {"position": "left-1/2", "text": "RFP"},
        {"position": "left-2/3", "text": "Pilot"},
        {"position": "right-1/6", "text": "Déploiement"}
    ]

    return render_template('timeline.html', projects=projects, periods=periods, milestones=milestones)

@app.route('/etp')
def etp_table():
    # Utiliser les mêmes données que la timeline
    projects = [
        {
            "name": "Procurement",
            "tasks": [
                {"start": 2, "width": 2, "color": "blue-600", "text": "Analyse contrats & RFI (1 ETP)"},
                {"start": 4, "width": 2, "color": "blue-500", "text": "RFP & Négociations (1 ETP)"}
            ]
        },
        {
            "name": "Workforce & HR",
            "tasks": [
                {"start": 1, "width": 1, "color": "purple-600", "text": "Initiation (1 ETP)"},
                {"start": 2, "width": 2, "color": "purple-500", "text": "Analyse & Design (2 ETP)"},
                {"start": 4, "width": 3, "color": "purple-400", "text": "Accompagnement & Déploiement (2 ETP)"}
            ]
        },
        {
            "name": "EUS",
            "tasks": [
                {"start": 2, "width": 2, "color": "green-600", "text": "Due Diligence (3 ETP)"},
                {"start": 4, "width": 1, "color": "green-500", "text": "RFP (3 ETP)"},
                {"start": 5, "width": 2, "color": "green-400", "text": "Pilot & Deploy (3 ETP)"}
            ]
        },
        {
            "name": "VIP/Events",
            "tasks": [
                {"start": 1, "width": 2, "color": "yellow-600", "text": "Analyse & Design (0.5 ETP)"}
            ]
        },
        {
            "name": "Employee Experience",
            "tasks": [
                {"start": 2, "width": 2, "color": "red-600", "text": "Benchmark & Design (2 ETP)"},
                {"start": 4, "width": 3, "color": "red-500", "text": "Implementation & Optimization (2 ETP)"}
            ]
        },
        {
            "name": "Process Data Analytics",
            "tasks": [
                {"start": 2, "width": 2, "color": "indigo-600", "text": "Audit & Roadmap (3 ETP)"},
                {"start": 4, "width": 3, "color": "indigo-500", "text": "Implementation & Migration (3 ETP)"}
            ]
        },
        {
            "name": "Observability",
            "tasks": [
                {"start": 2, "width": 2, "color": "teal-600", "text": "Strategy & Design (2 ETP)"},
                {"start": 4, "width": 3, "color": "teal-500", "text": "POC & Implementation (2 ETP)"}
            ]
        },
        {
            "name": "TOM",
            "tasks": [
                {"start": 2, "width": 2, "color": "gray-600", "text": "Analysis & Design (2 ETP)"},
                {"start": 4, "width": 3, "color": "gray-500", "text": "Implementation & Transition (2 ETP)"}
            ]
        }
    ]
    
    etp_data, period_totals = calculate_etp_per_period(projects)
    total_max_etp = sum(row["total"] for row in etp_data)
    
    return render_template('etp_table.html', 
                         etp_data=etp_data, 
                         period_totals=period_totals,
                         total_max_etp=total_max_etp)

if __name__ == '__main__':
    app.run(debug=True)
```

### timeline.html
```html
<!-- templates/timeline.html -->
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Timeline Danone</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <div class="timeline-container">
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
                         style="grid-column: {{ task.start }} / span {{ task.width }};">
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
</body>
</html>
```

### etp_table.html
```html
<!-- templates/etp_table.html -->
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tableau ETP - Danone</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <div class="container">
        <h1 class="page-title">Tableau des ETP par période</h1>
        <nav class="navigation">
            <a href="/" class="nav-link">← Retour à la Timeline</a>
        </nav>
        
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
                    <tr>
                        <td>{{ row.name }}</td>
                        <td class="text-center">{{ "%.2f"|format(row["2024 Q3-Q4"]) }}</td>
                        <td class="text-center">{{ "%.2f"|format(row["2025 Q1-Q2"]) }}</td>
                        <td class="text-center">{{ "%.2f"|format(row["2025 Q3-Q4"]) }}</td>
                        <td class="text-center">{{ "%.2f"|format(row["2026-2027"]) }}</td>
                        <td class="text-center bold">{{ "%.2f"|format(row.total) }}</td>
                    </tr>
                    {% endfor %}
                    <tr class="total-row">
                        <td class="bold">Total ETP par période</td>
                        <td class="text-center bold">{{ "%.2f"|format(period_totals["2024 Q3-Q4"]) }}</td>
                        <td class="text-center bold">{{ "%.2f"|format(period_totals["2025 Q1-Q2"]) }}</td>
                        <td class="text-center bold">{{ "%.2f"|format(period_totals["2025 Q3-Q4"]) }}</td>
                        <td class="text-center bold">{{ "%.2f"|format(period_totals["2026-2027"]) }}</td>
                        <td class="text-center bold">{{ "%.2f"|format(total_max_etp) }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
```

### styles.css
```css
/* static/styles.css */
.timeline-container {
    padding: 1rem;
    background-color: white;
}

/* Header avec périodes */
.header-container {
    margin-bottom: 2rem;
}

.periods-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    background-color: #312e81;
    color: white;
}

.period {
    padding: 0.5rem;
    text-align: center;
    border-right: 1px solid white;
}

.period:last-child {
    border-right: none;
}

/* Contenu timeline */
.timeline-content {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.project-row {
    display: flex;
    align-items: center;
}

.project-name {
    font-weight: bold;
    font-size: 0.875rem;
    width: 6rem;
}

.project-tasks {
    flex-grow: 1;
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 0.25rem;
}

.task {
    color: white;
    font-size: 0.75rem;
    padding: 0.25rem;
}

/* Couleurs de fond */
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

/* Jalons */
.milestones {
    margin-top: 2rem;
}

.milestone-container {
    position: relative;
    height: 4rem;
}

.milestone {
    position: absolute;
    top: 0;
    transform: translateX(-50%);
}

.milestone-dot {
    width: 1rem;
    height: 1rem;
    background-color: #ef4444;
    border-radius: 50%;
    margin: 0 auto;
}

.milestone-text {
    font-size: 0.75rem;
    text-align: center;
    margin-top: 0.25rem;
}

/* Positions des jalons */
.left-1\/3 { left: 33.33%; }
.left-1\/2 { left: 50%; }
.left-2\/3 { left: 66.66%; }
.right-1\/6 { right: 16.66%; transform: translateX(50%); }

/* Styles pour le tableau ETP */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

.page-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 1rem;
}

.navigation {
    margin-bottom: 2rem;
}

.nav-link {
    color: #3b82f6;
    text-decoration: none;
}

.nav-link:hover {
    text-decoration: underline;
}

.etp-table-container {
    overflow-x: auto;
}

.etp-table {
    width: 100%;
    border-collapse: collapse;
    background-color: white;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.etp-table th,
.etp-table td {
    border: 1px solid #e5e7eb;
    padding: 0.5rem;
}

.etp-table th {
    background-color: #f3f4f6;
    font-weight: bold;
    text-align: left;
}

.text-center {
    text-align: center;
}

.bold {
    font-weight: bold;
}

.total-row {
    background-color: #f3f4f6;
}
```

