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