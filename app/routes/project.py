from flask import redirect, url_for
from flask import Blueprint, render_template, jsonify, request
from app.services import ProjectService, EtpService
from app.models import Project, Task
from app.constants import TimeConstants
from datetime import datetime, date
from app import db

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

    
@bp.route('/api/projects', methods=['POST'])
def create_project():
    try:
        data = request.json
        name = data.get('name')
        if not name:
            return jsonify({'error': 'Le nom du projet est requis'}), 400
            
        color_scheme = data.get('colorScheme', 'blue')
        project = ProjectService.create_project(name)
        
        return jsonify({
            'status': 'success',
            'project': {
                'id': project.id,
                'name': project.name
            }
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Erreur lors de la création du projet'}), 500
    
@bp.route('/api/tasks', methods=['POST'])
def create_task():
    try:
        data = request.json
        required_fields = ['project_id', 'text', 'start_date', 'end_date']
        
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Tous les champs requis doivent être renseignés'}), 400
        
        project_id = int(data['project_id'])
            
        # Conversion des dates
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        
        # Récupération du projet
        project = ProjectService.get_project_by_id(project_id)
        if not project:
            return jsonify({'error': 'Projet non trouvé'}), 404
            
        # Définir les couleurs disponibles pour le projet
        colors = ['blue', 'purple', 'green', 'yellow', 'red', 'indigo', 'teal', 'gray']
        default_color = colors[project_id % len(colors)]  # Utilise l'ID du projet pour choisir une couleur
        
        # Déterminer l'intensité en fonction du nombre de tâches existantes
        intensities = ['600', '500', '400']
        intensity = intensities[len(project.tasks) % len(intensities)]
        
        color = f"{default_color}-{intensity}"
        
        print(f"Creating task with color: {color}")
        
        task = ProjectService.create_task(
            project_id=project_id,
            text=data['text'],
            start_date=start_date,
            end_date=end_date,
            color=color,
            etp=float(data.get('etp', 1.0))
        )
        
        if task:
            task_dict = task.to_dict()
            print(f"Task created successfully: {task_dict}")
            return jsonify({
                'status': 'success',
                'task': task_dict
            }), 201
        else:
            raise Exception("La tâche n'a pas été créée correctement")
        
    except Exception as e:
        print(f"Error creating task: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/api/projects')
def get_projects():
    try:
        projects = ProjectService.get_all_projects()
        return jsonify({
            'status': 'success',
            'projects': [{'id': p.id, 'name': p.name} for p in projects]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    








@bp.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        data = request.json
        task = Task.query.get(task_id)
        
        if not task:
            return jsonify({'error': 'Tâche non trouvée'}), 404
            
        # Mise à jour des champs
        task.text = data.get('text', task.text)
        task.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        task.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        task.etp = float(data.get('etp', task.etp))
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'task': task.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        success = ProjectService.delete_task(task_id)
        
        if success:
            return jsonify({'status': 'success'})
        else:
            return jsonify({'error': 'Tâche non trouvée'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500