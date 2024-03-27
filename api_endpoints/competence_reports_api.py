from datetime import datetime
from operator import and_
import uuid
from apiflask import APIBlueprint
from flask import jsonify
from app import db
from auth_middleware import token_required
from models.pupil import Pupil
from models.competence import CompetenceReport, CompetenceCheck
from models.schoolday import SchoolSemester
from schemas.competence_schemas import *

competence_report_api = APIBlueprint('competence_report_api', __name__, url_prefix='/api/competence_reports')

#- POST COMPETENCE REPORT
#########################
@competence_report_api.route('/<internal_id>', methods=['POST'])
@competence_report_api.doc(security='ApiKeyAuth', tags=['Competence Report'], summary='Post a competence report')
@token_required
def post_competence_report(current_user, internal_id, json_data):
    pupil = Pupil.query.filter_by(internal_id = internal_id).first()
    if pupil == None:
        return jsonify({'message': 'Dieses Kind existiert nicht!'}), 404
    pupil_id = pupil.internal_id
    report_id = str(uuid.uuid4().hex)
    created_by = current_user.name
    data = json_data
    created_at = data['created_at']
    created_at = datetime.strptime(created_at, '%Y-%m-%d').date() 
    school_semester = db.session.query(SchoolSemester).filter(and_(
        created_at >= SchoolSemester.start_date,
        created_at <= SchoolSemester.end_date)).first()
    if school_semester is None:
        return jsonify({'message' : 'Das Datum ist nicht innerhalb eines Schulhalbjahres!'}),404

    competence_checks = db.session.query(CompetenceCheck).filter(and_(
    CompetenceCheck.created_at >= school_semester.start_date,
    CompetenceCheck.created_at <= school_semester.end_date,
    CompetenceCheck.is_report == True)).all()
    new_competence_report = CompetenceReport(report_id, created_by, created_at, pupil_id, school_semester.id)
    new_competence_report.competence_checks.extend(competence_checks)
    db.session.add(new_competence_report)
    db.session.commit()
    return competence_report_schema.jsonify(new_competence_report)

#- GET ALL COMPETENCE REPORTS
#############################
@competence_report_api.route('/all', methods=['GET'])
@competence_report_api.doc(security='ApiKeyAuth', tags=['Competence Report'], summary='Get all competence reports')
@token_required
def get_competence_reports(current_user):
    
    all_reports = CompetenceReport.query.all()
    if all_reports == []:
        return jsonify({'message': 'No reports found!'}), 404
    result = competence_report_schema.dump(all_reports)
    return jsonify(result)

#- GET ALL COMPETENCE REPORTS FROM ONE PUPIL
############################################
@competence_report_api.route('/<internal_id>/all', methods=['GET'])
@competence_report_api.doc(security='ApiKeyAuth', tags=['Competence Report'], summary='Get all competence reports')
@token_required
def get_pupil_competence_reports(current_user, internal_id):

    pupil_reports = CompetenceReport.query.filter_by(pupil_id = internal_id).all()
    if pupil_reports == []:
        return jsonify({'message': 'No reports found!'}), 404
    result = competence_report_schema.dump(pupil_reports)
    return jsonify(result)