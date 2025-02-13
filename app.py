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