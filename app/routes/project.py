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