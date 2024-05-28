
from datetime import datetime
import os
import uuid
from sqlalchemy.sql import exists
from apiflask import APIBlueprint, FileSchema, abort
from flask import current_app, jsonify, request, send_file
from app import db
from models.log_entry import LogEntry
from models.schoolday import Admonition, Schoolday
from models.pupil import Pupil
from schemas.admonition_schemas import *
from schemas.pupil_schemas import *
from auth_middleware import token_required
from schemas.schemas import ApiFileSchema

admonition_api = APIBlueprint('admonitions_api', __name__, url_prefix='/api/admonition')

#- POST ADMONITION  
##################
@admonition_api.route('/new', methods=['POST'])
@admonition_api.input(admonition_in_schema, example={
  "admonished_day": "2023-08-07",
  "admonished_pupil_id": 1234,
  "admonition_reason": "kodiert",
  "admonition_type": "kodiert",
  "file_url": None,
  "processed_file_url": None,
  "processed": False,
  "processed_at": None,
  "processed_by": None
})
@admonition_api.output(pupil_schema)
@admonition_api.doc(security='ApiKeyAuth', tags=['Admonitions'], summary='Post an admonition')
@token_required
def add_admonition(current_user, json_data):
    admonishing_user = current_user.name
    admonished_pupil_id = json_data['admonished_pupil_id']
    if db.session.query(exists().where(Pupil.internal_id == admonished_pupil_id)).scalar() == False:
        return jsonify( {"message": "This pupil does not exist!"}), 404
    admonished_day = json_data['admonished_day']
    this_schoolday = db.session.query(Schoolday).filter(Schoolday.schoolday == admonished_day ).first()
    if this_schoolday == None:
        return jsonify( {"message": "This schoolday does not exist!"}), 404
    admonished_day_id = this_schoolday.schoolday
    admonition_id = str(uuid.uuid4().hex)   
    admonition_type = json_data['admonition_type']
    admonition_reason = json_data['admonition_reason']
    processed = False
    processed_by = None
    processed_at = None
    file_url = None
    processed_file_url = None
    new_admonition = Admonition(admonition_id, admonished_pupil_id, admonished_day_id, admonition_type, admonition_reason, admonishing_user, processed, processed_by, processed_at, file_url, processed_file_url)
    db.session.add(new_admonition)
    db.session.commit()
    pupil = Pupil.query.filter_by(internal_id = admonished_pupil_id).first()
    return pupil

#- GET ADMONITIONS
##################
@admonition_api.route('/all', methods=['GET'])
@admonition_api.output(admonitions_schema)
@admonition_api.doc(security='ApiKeyAuth', tags=['Admonitions'], summary='Get all admonitions')
@token_required
def get_admonitions(current_user):
    all_admonitions = Admonition.query.all()
    if all_admonitions == []:
        return jsonify({'message': 'Keine Ereignisse gefunden!'}),404
    result = admonitions_schema.dump(all_admonitions)
    return jsonify(result)

#- GET ONE ADMONITION
#####################
@admonition_api.route('/<admonition_id>', methods=['GET'])
@admonition_api.output(admonition_schema)
@admonition_api.doc(security='ApiKeyAuth', tags=['Admonitions'], summary='Get an admonition by id')
@token_required
def get_admonition(current_user, admonition_id):
    this_admonition = db.session.query(Admonition).filter(Admonition.admonition_id == admonition_id ).first() 
    if this_admonition == None:
        return jsonify({'message': 'Diese Ermahnung existiert nicht!'}), 404
    return admonition_schema.jsonify(this_admonition)

#- PATCH ADMONITION  
###################
@admonition_api.route('/<admonition_id>/patch', methods=['PATCH'])
@admonition_api.input(admonition_patch_schema)
@admonition_api.output(pupil_schema)
@admonition_api.doc(security='ApiKeyAuth',tags=['Admonitions'], summary='Patch an admonition')
@token_required
def patch_admonition(current_user, admonition_id, json_data):
    admonition = db.session.query(Admonition).filter(Admonition.admonition_id == admonition_id ).first() 
    if admonition is None:
        return jsonify( {"message": "An admonition with this date and this student does not exist!"}), 404  
    data = json_data
    for key in data:
        match key:
            case 'admonition_type': 
                admonition.admonition_type = data[key]
            case 'admonition_reason':
                admonition.admonition_reason = data[key]
            case 'processed':
                admonition.processed = data[key]
            case 'processed_by':
                admonition.processed_by = data[key]
            case 'processed_at':
                admonition.processed_at = data[key]
            case 'admonishing_user':
                admonition.admonishing_user = data[key]
            case 'file_url':
                admonition.file_url = data[key]
            case 'processed_file_url':
                admonition.processed_file_url = data[key]
    db.session.commit()
    pupil = Pupil.query.filter_by(internal_id = admonition.admonished_pupil_id).first()
    return pupil

#- PATCH ADMONITION FILE
########################
@admonition_api.route('/<admonition_id>/file', methods=['PATCH'])
@admonition_api.input(ApiFileSchema, location='files')
@admonition_api.output(pupil_schema)
@admonition_api.doc(security='ApiKeyAuth',tags=['Admonitions'], summary='PATCH-POST a file to document a given pupil admonition')
@token_required
def upload_admonition_file(current_user, admonition_id, files_data):
    admonition = db.session.query(Admonition).filter(Admonition.admonition_id == admonition_id ).first() 
    if admonition is None:
        return jsonify( {"message": "An admonition with this date and this student does not exist!"}), 404
    if 'file' not in files_data:
        abort(400, message="Keine Datei angegeben!")
    file = files_data['file']
    filename = str(uuid.uuid4().hex) + '.jpg'
    file_url = current_app.config['UPLOAD_FOLDER'] + '/admn/' + filename
    file.save(file_url)
    if len(str(admonition.file_url)) > 4:
        os.remove(str(admonition.file_url))
    admonition.file_url = file_url
    db.session.commit()
    pupil = Pupil.query.filter_by(internal_id = admonition.admonished_pupil_id).first()
    return pupil

#- PATCH ADMONITION PROCESSED FILE
##################################
@admonition_api.route('/<admonition_id>/processed_file', methods=['PATCH'])
@admonition_api.input(ApiFileSchema, location='files')
@admonition_api.output(pupil_schema)
@admonition_api.doc(security='ApiKeyAuth',tags=['Admonitions'], summary='PATCH-POST a file to document a given pupil processed admonition')
@token_required
def upload_admonition_processed_file(current_user, admonition_id, files_data):
    admonition = db.session.query(Admonition).filter(Admonition.admonition_id == admonition_id ).first() 
    if admonition is None:
        return jsonify( {"message": "An admonition with this date and this student does not exist!"}), 404
    if 'file' not in files_data:
        abort(400, message="Keine Datei angegeben!")
    file = files_data['file']
    filename = str(uuid.uuid4().hex) + '.jpg'
    file_url = current_app.config['UPLOAD_FOLDER'] + '/admn/' + filename
    file.save(file_url)
    if len(str(admonition.processed_file_url)) > 4:
        os.remove(str(admonition.processed_file_url))
    admonition.processed_file_url = file_url
    db.session.commit()
    pupil = Pupil.query.filter_by(internal_id = admonition.admonished_pupil_id).first()
    return pupil

#- GET ADMONITION FILE
######################
@admonition_api.route('/<admonition_id>/file', methods=['GET'])
@admonition_api.output(FileSchema, content_type='image/jpeg')
@admonition_api.doc(security='ApiKeyAuth', tags=['Admonitions'], summary='Get file of a given admonition')
@token_required
def download_admonition_file(current_user,admonition_id):
    admonition = db.session.query(Admonition).filter(Admonition.admonition_id == 
                                            admonition_id).first()
    if admonition == None:
        abort(404, message="An admonition with this date and this pupil does not exist!")        
    if len(str(admonition.file_url)) < 5:
        abort(404, message="This admonition has no file!") 
    url_path = admonition.file_url
    return send_file(url_path, mimetype='image/jpg')

#- GET ADMONITION PROCESSED FILE
################################
@admonition_api.route('/<admonition_id>/processed_file', methods=['GET'])
@admonition_api.output(FileSchema, content_type='image/jpeg')
@admonition_api.doc(security='ApiKeyAuth', tags=['Admonitions'], summary='Get file of a given processed admonition')
@token_required
def download_admonition_processed_file(current_user,admonition_id):
    admonition = db.session.query(Admonition).filter(Admonition.admonition_id == 
                                            admonition_id).first()
    if admonition == None:
        abort(404, message="An admonition with this date and this pupil does not exist!")        
    if len(str(admonition.processed_file_url)) < 5:
        abort(404, message="This admonition has no processed file!") 
    url_path = admonition.processed_file_url
    return send_file(url_path, mimetype='image/jpg')

#- DELETE ADMONITION FILE
#########################
@admonition_api.route('/<admonition_id>/file', methods=['DELETE'])
@admonition_api.output(pupil_schema)
@admonition_api.doc(security='ApiKeyAuth', tags=['Admonitions'], summary='Delete admonition file of a given admonition')
@token_required
def delete_admonition_file(current_user, admonition_id):
    if not current_user:
        abort(404, message='Bitte erneut einloggen!')
    admonition = db.session.query(Admonition).filter(Admonition.admonition_id == admonition_id ).first() 
    if admonition is None:
        return jsonify( {"message": "An admonition with this date and this student does not exist!"}), 404
    if len(str(admonition.file_url)) < 5:
        abort(404, message='This admonition has no file!')       
    if len(str(admonition.file_url)) > 4:
        os.remove(str(admonition.file_url))
    admonition.file_url = None
    #- LOG ENTRY
    log_datetime = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    user = current_user.name
    endpoint = request.method + ': ' + request.path
    payload = 'none'
    new_log_entry = LogEntry(datetime= log_datetime, user=user, endpoint=endpoint, payload=payload)
    db.session.add(new_log_entry)
    db.session.commit()
    pupil = Pupil.query.filter_by(internal_id = admonition.admonished_pupil_id).first()
    return pupil

#- DELETE ADMONITION PROCESSED FILE
###################################
@admonition_api.route('/<admonition_id>/processed_file', methods=['DELETE'])
@admonition_api.output(pupil_schema)
@admonition_api.doc(security='ApiKeyAuth', tags=['Admonitions'], summary='Delete admonition file of a given processed admonition')
@token_required
def delete_admonition_processed_file(current_user, admonition_id):
    if not current_user:
        abort(404, message='Bitte erneut einloggen!')
    admonition = db.session.query(Admonition).filter(Admonition.admonition_id == admonition_id ).first() 
    if admonition is None:
        return jsonify( {"message": "An admonition with this date and this student does not exist!"}), 404
    if len(str(admonition.processed_file_url)) < 5:
        abort(404, message='This admonition has no file!')       
    if len(str(admonition.processed_file_url)) > 4:
        os.remove(str(admonition.processed_file_url))
    admonition.processed_file_url = None
    #- LOG ENTRY
    log_datetime = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    user = current_user.name
    endpoint = request.method + ': ' + request.path
    payload = 'none'
    new_log_entry = LogEntry(datetime= log_datetime, user=user, endpoint=endpoint, payload=payload)
    db.session.add(new_log_entry)
    db.session.commit()
    pupil = Pupil.query.filter_by(internal_id = admonition.admonished_pupil_id).first()
    return pupil

#- DELETE ADMONITION
####################
@admonition_api.route('/<admonition_id>/delete', methods=['DELETE'])
@admonition_api.output(pupil_schema)
@admonition_api.doc(security='ApiKeyAuth', tags=['Admonitions'], summary='Delete an admonition and eventual file')
@token_required
def delete_admonition(current_user, admonition_id):
    admonition = db.session.query(Admonition).filter(Admonition.admonition_id == 
                                            admonition_id).first()
    pupil = db.session.query(Pupil).filter(Pupil.internal_id == admonition.admonished_pupil_id).first()                                   
    if admonition is None:
        return jsonify( {"message": "An admonition with this date and this student does not exist!"}), 404      
    if admonition.file_url is not None:
        os.remove(str(admonition.file_url))
    if admonition.processed_file_url is not None:
        os.remove(str(admonition.processed_file_url))
    db.session.delete(admonition)
    db.session.commit()
    return pupil
