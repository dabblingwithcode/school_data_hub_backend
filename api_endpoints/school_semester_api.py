from datetime import datetime
from apiflask import APIBlueprint
from flask import jsonify, request
from app import db
from auth_middleware import token_required
from schemas.schoolday_schemas import *
from models.schoolday import Schoolday, SchoolSemester

school_semester_api = APIBlueprint('school_semester_api', __name__, url_prefix='/api/school_semester')

#- POST SCHOOL SEMESTER
########################
@school_semester_api.route('/new', methods=['POST'])
@school_semester_api.doc(security='ApiKeyAuth', tags=['School Semester'], summary='Post a school semester')
@school_semester_api.input(school_semester_schema)
@school_semester_api.output(school_semester_schema)
@token_required
def add_school_semester(current_user, json_data): 
    start_date = json_data['start_date']
    end_date = json_data['end_date']
# Parse date strings to datetime objects
    print(start_date, end_date)
    # start_date_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
    # end_date_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
    # Check for date overlap with existing school semesters
    if check_date_overlap(start_date, end_date):
        return jsonify({"message": "Date range overlaps with an existing semester."}), 400
    # Retrieve Schoolday records for start and end dates
    start_date_schoolday = db.session.query(Schoolday).filter(Schoolday.schoolday == start_date).first()
    end_date_schoolday = db.session.query(Schoolday).filter(Schoolday.schoolday == end_date).first()
    if start_date_schoolday is None or end_date_schoolday is None:
        return jsonify({"message": "One or both date values do not exist!"}), 404
    # Create a new school semester
    is_first = json_data['is_first']
    new_school_semester = SchoolSemester(start_date_schoolday.schoolday, end_date_schoolday.schoolday, is_first)
    db.session.add(new_school_semester)
    db.session.commit()
    return new_school_semester
   
def check_date_overlap(start_date, end_date):
    existing_semesters = db.session.query(SchoolSemester).filter(
        ((start_date >= SchoolSemester.start_date) & (start_date <= SchoolSemester.end_date)) |
        ((end_date >= SchoolSemester.start_date) & (end_date <= SchoolSemester.end_date))
    )
    return existing_semesters.count() > 0


#- GET SCHOOL SEMESTERS
########################
@school_semester_api.route('/all', methods=['GET'])
@school_semester_api.output(school_semesters_schema)
@school_semester_api.doc(security='ApiKeyAuth', tags=['School Semester'], summary='Get all school semesters')
@token_required
def get_school_semesters(current_user) :
    all_semesters = db.session.query(SchoolSemester).all()
    if all_semesters == []:
        return jsonify({'error': 'No school semesters found!'})    
    result = school_semesters_schema.dump(all_semesters)
    return jsonify(result)
 