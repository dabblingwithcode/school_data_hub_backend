from datetime import datetime
from apiflask import APIBlueprint, abort
from flask import jsonify
from app import db
from schemas.schoolday_schemas import *
from models.schoolday import *
from auth_middleware import token_required

schoolday_api = APIBlueprint('schooldays_api', __name__, url_prefix='/api/schoolday')

#- POST SCHOOLDAY 
##################
@schoolday_api.route('/new', methods=['POST'])
@schoolday_api.input(schoolday_only_schema)
@schoolday_api.output(schoolday_only_schema)
@schoolday_api.doc(security='ApiKeyAuth', tags=['Schooldays'], summary='Post a schoolday')
@token_required
def add_schoolday(current_user, json_data) :
    schoolday = json_data['schoolday']
    stringtodatetime = datetime.strptime(schoolday, '%Y-%m-%d').date()
    exists = db.session.query(Schoolday).filter_by(schoolday= stringtodatetime).scalar() is not None 
    if exists == True:
        abort(400, message="Dieser Schultag existiert schon!")
    else:    
        new_schoolday = Schoolday(stringtodatetime) 
        db.session.add(new_schoolday)
        db.session.commit()
        #result = schoolday_only_schema.dump(new_schoolday)
        return new_schoolday
        #return schoolday_schema.jsonify(new_schoolday)
    
#- POST SCHOOLDAYS
###################
@schoolday_api.route('/new/list', methods=['POST'])
@schoolday_api.input(schooldays_only_schema)
@schoolday_api.output(schooldays_only_schema)
@schoolday_api.doc(security='ApiKeyAuth', tags=['Schooldays'], summary='Post multiple schooldays')
@token_required
def add_schooldays(current_user, json_data):
    schooldays = json_data['schooldays']
    new_schooldays = []
    for schoolday in schooldays:
        stringtodatetime = datetime.strptime(schoolday, '%Y-%m-%d').date()
        exists = db.session.query(Schoolday).filter_by(schoolday= stringtodatetime).scalar() is not None 
        if exists == True:
            abort(400, message="Dieser Schultag existiert schon!")
        else:    
            new_schoolday = Schoolday(stringtodatetime) 
            db.session.add(new_schoolday)
            new_schooldays.append(new_schoolday)
    db.session.commit()
    #result = schooldays_only_schema.dump(new_schoolday)
    return new_schooldays

#- GET ALL SCHOOLDAYS
#####################
@schoolday_api.route('/all', methods=['GET'])
@schoolday_api.output(schooldays_schema)
@schoolday_api.doc(security='ApiKeyAuth', tags=['Schooldays'], summary='Get all schooldays')
@token_required
def get_schooldays(current_user):
    if not current_user:
        abort(404, message='Bitte erneut einloggen!')
    all_schooldays = db.session.query(Schoolday).all()
    if all_schooldays == []:
        return jsonify({'error': 'No schooldays found!'})    
    #result = schooldays_schema.dump(all_schooldays)
    return all_schooldays

#- GET ALL SCHOOLDAYS - ONLY
############################
@schoolday_api.route('/all/flat', methods=['GET'])
@schoolday_api.output(schooldays_only_schema)
@schoolday_api.doc(security='ApiKeyAuth', tags=['Schooldays'], summary='Get a list of schooldays without nesting')
@token_required
def get_schooldays_only(current_user):
    if not current_user:
        abort(404, message='Bitte erneut einloggen!')
    all_schooldays = db.session.query(Schoolday).all()
    if all_schooldays == []:
        return jsonify({'error': 'No schooldays found!'})
    # result = schooldays_only_schema.dump(all_schooldays)
    return all_schooldays

#- GET ONE SCHOOLDAY WITH CHILDREN
##################################
@schoolday_api.route('/<date>', methods=['GET'])
@schoolday_api.output(schoolday_schema)
@schoolday_api.doc(security='ApiKeyAuth', tags=['Schooldays'], summary='Get a schoolday with nested elements')
@token_required
def get_schooday(current_user, date):
    stringtodatetime = datetime.strptime(date, '%Y-%m-%d').date()
    #- If date has wrong format and strptime fails, we're screwed :-/
    this_schoolday = db.session.query(Schoolday).filter(Schoolday.schoolday == stringtodatetime ).first()
    if this_schoolday == None:
        abort(404, message="Dieser Schultag existiert nicht!")
    return this_schoolday

#- DELETE ONE SCHOOLDAY
#######################
@schoolday_api.route('/<date>', methods=['DELETE'])
@schoolday_api.doc(security='ApiKeyAuth', tags=['Schooldays'], summary='Delete a schoolday with nested elements')
@token_required
def delete_schoolday(current_user, date):
    if not current_user.admin:
        return jsonify({'message' : 'Not authorized!'}), 401
    stringtodatetime = datetime.strptime(date, '%Y-%m-%d').date()
    this_schoolday = db.session.query(Schoolday).filter(Schoolday.schoolday == stringtodatetime ).first()
    if this_schoolday == None:
        return jsonify({'message': 'This schoolday does not exist!'}),404
    db.session.delete(this_schoolday)
    db.session.commit()
    return jsonify( {"message": "The schoolday was deleted!"}), 200

#- DELETE LIST OF SCHOOLDAYS
############################
@schoolday_api.route('/delete/list', methods=['DELETE'])
@schoolday_api.input(schooldays_only_schema)
@schoolday_api.doc(security='ApiKeyAuth', tags=['Schooldays'], summary='Delete multiple Schooldays')
@token_required
def delete_schooldays(current_user, json_data):
    if not current_user.admin:
        return jsonify({'message' : 'Not authorized!'}), 401
    schooldays = json_data['schooldays']
    for schoolday in schooldays:
        stringtodatetime = datetime.strptime(schoolday, '%Y-%m-%d').date()
        this_schoolday = db.session.query(Schoolday).filter(Schoolday.schoolday == stringtodatetime ).first()
        if this_schoolday == None:
            continue # return jsonify({'message': 'This schoolday does not exist!'}),404
        db.session.delete(this_schoolday)
    db.session.commit()
    return jsonify( {"message": "The schooldays were deleted!"}), 200
