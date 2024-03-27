from datetime import datetime
import os
import uuid
from apiflask import APIBlueprint, FileSchema, abort
from flask import current_app, send_file
from app import db
from auth_middleware import token_required
from schemas.pupil_schemas import *
from schemas.goal_schemas import *
from models.pupil import Pupil
from models.category import PupilCategoryStatus, GoalCategory
from schemas.schemas import ApiFileSchema

category_status_api = APIBlueprint('category_status_api', __name__, url_prefix='/api/category/statuses')

#- POST GATEGORY STATUS
#######################
@category_status_api.route('/<internal_id>/<category_id>', methods=['POST'])
@category_status_api.input(pupil_category_status_in_schema)
@category_status_api.output(pupil_schema)
@category_status_api.doc(security='ApiKeyAuth', tags=['Category Statuses'], summary='Post a status for a given catagory from a given pupil')
@token_required
def add_category_state(current_user, internal_id, category_id, json_data):
    this_pupil = Pupil.query.filter_by(internal_id = internal_id).first()
    if this_pupil == None:
        abort(400, message="Diese/r Schüler/in existiert nicht!")
    pupil_id = internal_id
    this_category = GoalCategory.query.filter_by(category_id = category_id).first()
    if this_category == None:
        abort(400, message="Diese Kategorie existiert nicht!")

    # category_status_exists = db.session.query(PupilCategoryStatus).filter(PupilCategoryStatus.pupil_id == internal_id, PupilCategoryStatus.goal_category_id == category_id ).first() is not None
    # if category_status_exists == True :
    #     return jsonify( {"message": "This category status exists already - please update instead!"}), 400
    goal_category_id = category_id
    status_id = uuid.uuid4().hex
    data = json_data
    state = data['state']
    comment = data['comment']
    created_at = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d').date() 
    created_by = current_user.name
    # created_at = datetime.strptime(created_at, '%Y-%m-%d').date()
    new_category_status = PupilCategoryStatus(pupil_id, goal_category_id, status_id, state, created_by, created_at, comment, None)
    db.session.add(new_category_status)
    db.session.commit()
    return this_pupil
    
#- PATCH GATEGORY STATUS
########################
@category_status_api.route('/<status_id>', methods=['PATCH'])
@category_status_api.input(pupil_category_status_in_schema)
@category_status_api.output(pupil_category_status_schema)
@category_status_api.doc(security='ApiKeyAuth', tags=['Category Statuses'], summary='Patch a status for a given catagory from a given pupil')
@token_required
def put_category_state(current_user, status_id, json_data):

    status = PupilCategoryStatus.query.filter_by(status_id = status_id).first()
    if status == None:
        abort(400, message="Dieser Kategoriestatus existiert nicht!")
    data = json_data
    for key in data:
        match key:
            case 'state':
                status.state = data['state']
            case 'comment':
                status.comment = data['comment']
    db.session.commit()
    return status

#- PATCH FILE CATEGORY STATUS 
#############################
@category_status_api.route('/<status_id>/file', methods=['PATCH'])
@category_status_api.input(ApiFileSchema, location='files')
@category_status_api.output(pupil_category_status_schema)
@category_status_api.doc(security='ApiKeyAuth', tags=['Category Statuses'], summary='PATCH-POST a file to document a given pupil category status')
@token_required
def upload_category_status_file(current_user, status_id, files_data):
    status = PupilCategoryStatus.query.filter_by(status_id = status_id).first()
    if status == None:
        abort(400, message="Dieser Kategoriestatus existiert nicht!")
    if 'file' not in files_data:
        abort(400, message="Keine Datei angegeben!")
    file = files_data['file']   
    filename = str(uuid.uuid4().hex) + '.jpg'
    file_url = current_app.config['UPLOAD_FOLDER'] + '/catg/' + filename
    file.save(file_url)
    if len(str(status.file_url)) > 4:
        os.remove(str(status.file_url))
    status.file_url = file_url
    db.session.commit()
    return status

#- GET FILE CATEGORY STATUS 
###########################
@category_status_api.route('/<status_id>/file', methods=['GET'])
@category_status_api.output(FileSchema, content_type='image/jpeg')
@category_status_api.doc(security='ApiKeyAuth', tags=['Category Statuses'], summary='Get file of a given pupil category status')
@token_required
def download_category_status_file(current_user, status_id):
    status = PupilCategoryStatus.query.filter_by(status_id = status_id).first()
    if status == None:
        abort(400, message="Dieser Kategoriestatus existiert nicht!")
    if len(str(status.file_url)) < 5:
        abort(400, message="Dieser Kategoriestatus hat keine Datei!")
       
    url_path = status.file_url
    return send_file(url_path, mimetype='image/jpg')

#- DELETE GATEGORY STATUS
#########################
@category_status_api.route('/<status_id>/delete', methods=['DELETE'])
@category_status_api.output(pupil_schema, 200)
@category_status_api.doc(security='ApiKeyAuth', tags=['Category Statuses'], summary='Delete a status for a given catagory from a given pupil')
@token_required
def delete_category_status(current_user, status_id):
    status = PupilCategoryStatus.query.filter_by(status_id = status_id).first()
    pupil = Pupil.query.filter_by(internal_id = status.pupil_id).first()
    if status == None:
        abort(400, message="Dieser Kategoriestatus existiert nicht!")
    db.session.delete(status)
    db.session.commit()
    return pupil
