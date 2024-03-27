from datetime import datetime
import os
import uuid
from models.log_entry import LogEntry
from schemas.schemas import ApiFileSchema
from schemas.workbook_schemas import *
from models.workbook import Workbook
from apiflask import APIBlueprint, FileSchema, abort
from flask import current_app, json, jsonify, request, send_file
from app import db
from auth_middleware import token_required

workbook_api = APIBlueprint('workbooks_api', __name__, url_prefix='/api/workbook')

#- GET WORKBOOKS 
################

@workbook_api.route('/all', methods=['GET'])
@workbook_api.output(workbooks_schema)
@workbook_api.doc(security='ApiKeyAuth', tags=['Workbooks'], summary='get workbooks with nested working pupils')
@token_required
def get_workbooks(current_user):
    if not current_user:
        abort(404, message='Bitte erneut einloggen!')
    all_workbooks = Workbook.query.all()
    if all_workbooks == []:
        return jsonify({'error': 'No workbooks found!'}), 404
    result = workbooks_schema.dump(all_workbooks)
    return jsonify(result)

#- GET WORKBOOKS FLAT
#####################

@workbook_api.route('/all/flat', methods=['GET'])
@workbook_api.output(workbooks_flat_schema)
@workbook_api.doc(security='ApiKeyAuth', tags=['Workbooks'], summary='get workbooks without nested working pupils')
@token_required
def get_workbooks_flat(current_user):
    if not current_user:
        abort(404, message='Bitte erneut einloggen!')
    all_workbooks = Workbook.query.all()
    if all_workbooks == []:
        return jsonify({'error': 'No workbooks found!'}), 404
    # result = workbooks_flat_schema.dump(all_workbooks)
    # return jsonify(result)
    return all_workbooks

#- GET ONE WORKBOOK
###################

@workbook_api.route('/<isbn>', methods=['GET'])
@workbook_api.output(workbook_flat_schema)
@workbook_api.doc(security='ApiKeyAuth', tags=['Workbooks'], summary='Get one workbook')
@token_required
def get_one_workbook(current_user, isbn):
    if not current_user:
        abort(404, message='Bitte erneut einloggen!')
    workbook = Workbook.query.filter_by(isbn=isbn).first()
    if workbook == None:
        return jsonify({'error': 'No workbook found!'}), 404
    result = workbook_flat_schema.dump(workbook)
    return jsonify(result)


#- POST WORKBOOK
################

@workbook_api.route('/new', methods=['POST'])
@workbook_api.input(workbook_flat_schema)
@workbook_api.output(workbook_flat_schema)
@workbook_api.doc(security='ApiKeyAuth', tags=['Workbooks'], summary='Post a new workbook')
@token_required
def create_workbook(current_user, json_data):
    data = json_data
    isbn = data['isbn']
    name = data['name']
    subject = data['subject']
    level = data['level']
    image_url = data['image_url']
    if db.session.query(Workbook).filter_by(isbn= isbn).scalar() is not None:
        return jsonify({'message': 'Das Arbeitsheft existiert schon!'}), 400
    new_workbook = Workbook(isbn, name, subject, level, image_url)
    db.session.add(new_workbook)
  
    #- LOG ENTRY
    log_datetime = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    user = current_user.name
    endpoint = request.method + ': ' + request.path
    payload = json.dumps(data, indent=None, sort_keys=True)
    new_log_entry = LogEntry(datetime= log_datetime, user=user, endpoint=endpoint, payload=payload)
    db.session.add(new_log_entry)

    db.session.commit()
    return new_workbook

#- PATCH WORKBOOK 
#################

@workbook_api.route('/<isbn>', methods=['PATCH'])
@workbook_api.input(workbook_flat_schema)
@workbook_api.output(workbook_flat_schema)
@workbook_api.doc(security='ApiKeyAuth', tags=['Workbooks'], summary='Patch an existing workbook')
@token_required
def patch_workbook(current_user, isbn, json_data):
    workbook = db.session.query(Workbook).filter_by(isbn= isbn).scalar()
    if workbook is None:
        return jsonify({'message': 'Das Arbeitsheft existiert nicht!'}), 404
    data = request.get_json()
    for key in data:
        match key:
            case 'name':
                workbook.name = data['name']  
            case 'subject':
                workbook.subject = data['subject']
            case 'level':
                workbook.level = data['level']
            case 'image_url':
                workbook.image_url = data['image_url']
    db.session.commit()
    return workbook_flat_schema.jsonify(workbook)

#- PATCH WORKBOOK WITH IMAGE
############################

@workbook_api.route('/<isbn>/image', methods=['PATCH'])
@workbook_api.input(ApiFileSchema, location='files')
@workbook_api.output(workbook_flat_schema)
@workbook_api.doc(security='ApiKeyAuth', tags=['Workbooks'], summary='Patch an existing workbook with image')
@token_required
def patch_workbook_image(current_user, isbn, files_data):
    workbook = db.session.query(Workbook).filter_by(isbn= isbn).scalar()
    if workbook is None:
        return jsonify({'message': 'Das Arbeitsheft existiert nicht!'}), 404
    if 'file' not in files_data:
        abort(400, message="Keine Datei angegeben!")
    file = files_data['file']
    filename = str(uuid.uuid4().hex) + '.jpg'
    file_url = current_app.config['UPLOAD_FOLDER'] + '/wrk/' + filename
    file.save(file_url)
    if len(str(workbook.image_url)) > 4:
        os.remove(str(workbook.image_url))
    workbook.image_url = file_url
    db.session.commit()
    return workbook

#- GET WORKBOOK IMAGE
#####################

@workbook_api.get('/<isbn>/image')
@workbook_api.output(FileSchema, content_type='image/jpeg')
@workbook_api.doc(security='ApiKeyAuth', tags=['Workbooks'], summary='Get workbook image')
@token_required
def get_workbook_image(current_user, isbn):
    workbook = db.session.query(Workbook).filter_by(isbn= isbn).scalar()
    if workbook is None:
        return jsonify({'message': 'Das Arbeitsheft existiert nicht!'}), 404
    if len(str(workbook.image_url)) < 5:
        abort(404, message="Keine Datei vorhanden!")
    return send_file(str(workbook.image_url), mimetype='image/jpg')


#- DELETE WORKBOOK
##################

@workbook_api.route('/<isbn>', methods=['DELETE'])
@workbook_api.doc(security='ApiKeyAuth', tags=['Workbooks'], summary='Delete a workbook')
@token_required
def delete_workbook(current_user, isbn):
    if not current_user.admin:
        return jsonify({'error' : 'Not authorized!'}), 401
    this_workbook = Workbook.query.filter_by(isbn = isbn).first()
    if this_workbook == None:
        return jsonify({'message': 'Dieses Arbeitsheft existiert nicht!'}), 404
    db.session.delete(this_workbook)
    db.session.commit()
    all_workbooks = Workbook.query.all()
    if all_workbooks == []:
        return jsonify({'error': 'No workbooks found!'}), 404
    result = workbooks_flat_schema.dump(all_workbooks)
    return jsonify(result)