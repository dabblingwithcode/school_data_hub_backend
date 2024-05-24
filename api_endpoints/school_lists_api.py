import uuid
from apiflask import APIBlueprint, abort
from flask import jsonify
from sqlalchemy.sql import exists
from app import db
from auth_middleware import token_required
from schemas.pupil_schemas import *
from schemas.school_list_schemas import *
from models.pupil import Pupil
from models.school_list import SchoolList, PupilList

school_list_api = APIBlueprint('school_list_api', __name__, url_prefix='/api/school_lists')

#- POST SCHOOL LIST WITH ALL PUPILS 
####################################
@school_list_api.route('/all', methods=['POST'])
@school_list_api.input(school_list_in_schema)
@school_list_api.output(school_list_flat_schema)
@school_list_api.doc(security='ApiKeyAuth', tags=['School Lists'], summary='Post a school list including ALL pupils in the database')
@token_required
def add_list_all(current_user, json_data):
    if not current_user.admin:
        abort(401, message="Keine Berechtigung!")
    data = json_data    
    list_name = data['list_name']
    existing_list = SchoolList.query.filter_by(list_name = list_name).first()
    if existing_list:
        abort(400, message="Die Liste existiert bereits!")
    list_id = str(uuid.uuid4().hex)
    list_description = data['list_description']
    visibility = data['visibility']   
    created_by = current_user.name
    authorized_users = None
    new_list = SchoolList(list_id, list_name, list_description, created_by, visibility, authorized_users)
    db.session.add(new_list)
    all_pupils = Pupil.query.all()
    for item in all_pupils:
        origin_list = list_id
        listed_pupil_id = item.internal_id
        pupil_list_status = None
        pupil_list_comment = None
        pupil_list_entry_by = None
        new_pupil_list = PupilList(pupil_list_status, pupil_list_comment, pupil_list_entry_by, origin_list, listed_pupil_id,)
        db.session.add(new_pupil_list)
    db.session.commit()    
    return new_list

#- POST SCHOOL LIST WITH LIST OF PUPILS
#######################################
@school_list_api.route('/list', methods=['POST'])
@school_list_api.input(school_list_in_group_schema)
@school_list_api.output(school_list_flat_schema)
@school_list_api.doc(security='ApiKeyAuth', tags=['School Lists'], summary='Post a school list including pupils from an array')
@token_required
def add_list_group(current_user, json_data):
    data = json_data
    list_name = data['list_name']
    existing_list = SchoolList.query.filter_by(list_name = list_name).first()
    if existing_list:
        abort(400, message="Die Liste existiert bereits!")       
    internal_id_list = data['pupils']
    list_id = str(uuid.uuid4().hex)
    list_description = data['list_description']
    visibility = data['visibility']
    created_by = current_user.name
    authorized_users = None
    new_list = SchoolList(list_id, list_name, list_description, created_by, visibility, authorized_users)
    db.session.add(new_list)
    #-We have to create the list to populate it with pupils.
    #-This is why it is created even if pupils are wrong and the list remains empty. 
    for item in internal_id_list:
        if db.session.query(exists().where(Pupil.internal_id == item)).scalar() == True:
            origin_list = list_id
            listed_pupil_id = item
            pupil_list_status = None
            pupil_list_comment = None
            pupil_list_entry_by = None
            new_pupil_list = PupilList(pupil_list_status, pupil_list_comment, pupil_list_entry_by,
                                       origin_list, listed_pupil_id)
            db.session.add(new_pupil_list)
    db.session.commit()
    return new_list

#- PATCH SCHOOL LIST 
#####################
@school_list_api.route('/<list_id>/patch', methods=['PATCH'])
@school_list_api.input(school_list_in_schema)
@school_list_api.output(school_list_flat_schema)
@school_list_api.doc(security='ApiKeyAuth', tags=['School Lists'], summary='Patch a school list')
@token_required
def patch_school_list(current_user, list_id, json_data):
    data = json_data
    existing_list = SchoolList.query.filter_by(list_id = list_id).first()
    if existing_list is None:
        abort(404, message="Die Liste existiert nicht!")
    for key in data:
        match key:
            case 'list_name':
                existing_list.list_name = data[key]
            case 'list_description':
                existing_list.list_description = data[key]
            case 'visibility':
                existing_list.visibility = data[key]
            case 'authorized_users':
                existing_list.authorized_users = data[key]   
    db.session.commit()
    return existing_list

#- GET ALL LISTS 
################
@school_list_api.route('/all', methods=['GET'])
@school_list_api.output(school_lists_schema)
@school_list_api.doc(security='ApiKeyAuth', tags=['School Lists'], summary='Get all school lists with nested elements')
@token_required
def get_lists(current_user):
    if not current_user:
        abort(404, message='Bitte erneut einloggen!')
    all_lists = SchoolList.query.all()
    if all_lists == []:
        abort(404, message="Keine Listen vorhanden!")
    return all_lists

#- GET ALL LISTS FLAT
#####################
@school_list_api.route('/all/flat', methods=['GET'])
@school_list_api.output(school_lists_flat_schema)
@school_list_api.doc(security='ApiKeyAuth', tags=['School Lists'], summary='Get all school lists without nested elements')
@token_required
def get_lists_flat(current_user):
    if not current_user:
        abort(404, message='Bitte erneut einloggen!')
    all_lists = SchoolList.query.all()
    if all_lists == []:
        abort(404, message="Keine Listen vorhanden!")
    return all_lists

#- POST PUPIL(S) TO LIST
########################
@school_list_api.route('/<list_id>/pupils', methods=['POST'])
@school_list_api.input(pupil_id_list_schema)
@school_list_api.output(pupils_schema)
@school_list_api.doc(security='ApiKeyAuth', tags=['School Lists'], summary='Add pupil(s) to a school list')
@token_required
def add_pupil_to_list(current_user, list_id, json_data):
    school_list = SchoolList.query.filter_by(list_id = list_id).first()
    if school_list == None:
        abort(404, message="Diese Liste existiert nicht!")
    data = json_data
    modified_pupils = []
    internal_id_list = data['pupils']
    if internal_id_list == []:
        abort(404, message="Keine Schueler angegeben!")
    for item in internal_id_list: 
        modified_pupil = Pupil.query.filter_by(internal_id = item).first()       
        if modified_pupil != None:
            if PupilList.query.filter_by(origin_list= list_id, listed_pupil_id= item).first() == None:
                origin_list = list_id
                listed_pupil_id = item
                pupil_list_status = None
                pupil_list_comment = None
                pupil_list_entry_by = None
                new_pupil_list = PupilList(pupil_list_status, pupil_list_comment, pupil_list_entry_by, origin_list, listed_pupil_id)
                db.session.add(new_pupil_list)
                modified_pupils.append(modified_pupil)
    db.session.commit()
    return modified_pupils

#- DELETE LIST 
##############
@school_list_api.route('/<list_id>', methods=['DELETE'])
@school_list_api.output(school_lists_schema)
@school_list_api.doc(security='ApiKeyAuth', tags=['School Lists'], summary='Delete a school list')
@token_required
def delete_list(current_user, list_id):
    this_list_id = list_id
    this_list = db.session.query(SchoolList).filter(SchoolList.list_id == this_list_id).first()
    if this_list == None:
        return jsonify( {"message": "The school list does not exist!"}), 404
    if current_user.name != this_list.created_by:
        abort(401, message="Keine Berechtigung!")
    for item in this_list.pupils_in_list:
        db.session.delete(item)
    db.session.delete(this_list)
    db.session.commit()
    all_lists = SchoolList.query.all()
    if all_lists == []:
        abort(404, message="Keine Listen vorhanden!")
    return all_lists
