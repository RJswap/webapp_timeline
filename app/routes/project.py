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
            
            # Mise à jour des couleurs des tâches
            for task in project.tasks:
                # Extraire l'intensité de la couleur actuelle
                intensity = task.color.split('-')[1]
                # Appliquer la nouvelle couleur avec la même intensité
                task.color = f"{data['colorScheme']}-{intensity}"
        
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
            etp=float(data.get('etp', 1.0)),
            comment=data.get('comment')
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
        
        # Mise à jour du projet si nécessaire
        if 'project_id' in data:
            new_project = Project.query.get(int(data['project_id']))
            if not new_project:
                return make_response(error='Nouveau projet non trouvé', status=404)
            
            # Si le projet a changé, mettre à jour la couleur de la tâche
            if task.project_id != new_project.id:
                # Conserver l'intensité de la couleur actuelle
                intensity = task.color.split('-')[1]
                task.color = f"{new_project.color_scheme}-{intensity}"
                task.project_id = new_project.id
            
        # Mise à jour des autres champs
        task.text = data.get('text', task.text)
        task.comment = data.get('comment', task.comment)
        task.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        task.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        task.etp = float(data.get('etp', task.etp))
        
        db.session.commit()
        
        return make_response(data={'task': task.to_dict()})
        
    except Exception as e:
        db.session.rollback()
        return make_response(error=str(e), status=500)

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