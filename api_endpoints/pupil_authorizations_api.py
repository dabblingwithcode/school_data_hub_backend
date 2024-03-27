from datetime import datetime
import os
import uuid
from apiflask import APIBlueprint, FileSchema, abort
from flask import current_app, request, send_file
from app import db
from auth_middleware import token_required
from models.log_entry import LogEntry
from models.pupil import  Pupil
from models.authorization import Authorization, PupilAuthorization
from schemas.schemas import ApiFileSchema
from schemas.pupil_schemas import *
from schemas.authorization_schemas import *

pupil_authorization_api = APIBlueprint('pupil_authorizations', __name__, url_prefix='/api/pupil_authorizations')

#-POST PUPIL AUTHORIZATION 
#############################
@pupil_authorization_api.route('/<internal_id>/<auth_id>/new', methods=['POST'])
@pupil_authorization_api.input(pupil_authorization_in_schema)
@pupil_authorization_api.output(pupil_schema)
@pupil_authorization_api.doc(security='ApiKeyAuth', tags=['Pupil Authorizations'], summary='Post authorization for a given pupil')
@token_required
def post_pupil_authorization(current_user, internal_id, auth_id,json_data):
    pupil = db.session.query(Pupil).filter(Pupil.internal_id == 
                                                internal_id).first()
    if pupil == None:
        abort(400, message='This pupil does not exist!')
        
    data = json_data # request.get_json()
    #origin_authorization = data['origin_authorization']
    duplicate = db.session.query(PupilAuthorization).filter(PupilAuthorization.pupil_id == 
                                                internal_id,
                                                PupilAuthorization.origin_authorization == auth_id).first()
    if duplicate != None:
        abort(400, message='This pupil authorization already exists!')        
    status = data['status']
    comment = data['comment']
    file_url = data['file_url']  
    #- HACKY FIX - this should be a nullable modified_by  
    created_by = ''
    authorization = PupilAuthorization(status=status, comment=comment, created_by=created_by, file_url=file_url, origin_authorization=auth_id, pupil_id=internal_id)
    db.session.add(authorization)
    db.session.commit()
    return pupil

#- POST PUPIL AUTHORIZATIONS FROM LIST OF PUPILS
################################################
@pupil_authorization_api.route('/<auth_id>/list', methods=['POST'])
@pupil_authorization_api.input(pupil_id_list_schema)
@pupil_authorization_api.output(pupils_schema)
@pupil_authorization_api.doc(security='ApiKeyAuth', tags=['Pupil Authorizations'], summary='Add pupils to an existing authorization')
@token_required
def add_pupils_to_authorization(current_user, auth_id, json_data):
    data = json_data
    existing_authorization = Authorization.query.filter_by(authorization_id = auth_id).first()
    if existing_authorization is None:
        abort(404, message="Diese Einwilligung existiert nicht!")        
    pupil_id_list = data['pupils']
    if pupil_id_list == []:
       abort(404, message="Keine Schueler angegeben!")
    added_pupils = []
    for item in pupil_id_list:
        pupil = Pupil.query.filter_by(internal_id = item).first()
        if pupil is not None:
            if PupilAuthorization.query.filter_by(origin_list= auth_id, listed_pupil_id= item).first() == None:
                origin_authorization = auth_id
                pupil_id = item
                status = None
                comment = None
                #- HACKY FIX - this should be a nullable modified_by
                created_by = ''
                new_pupil_authorization = PupilAuthorization(origin_authorization=origin_authorization, pupil_id=pupil_id, status=status, comment=comment, created_by=created_by, file_url=None)
                db.session.add(new_pupil_authorization)
                added_pupils.append(pupil)
    db.session.commit()    
    return added_pupils

#- DELETE PUPIL AUTHORIZATION
#############################
@pupil_authorization_api.route('/<internal_id>/<auth_id>', methods=['DELETE'])
@pupil_authorization_api.output(pupil_schema)
@pupil_authorization_api.doc(security='ApiKeyAuth', tags=['Pupil Authorizations'], summary='Delete an authorization for a given pupil')
@token_required
def delete_pupil_authorization(current_user, internal_id, auth_id):
    pupil = db.session.query(Pupil).filter(Pupil.internal_id == 
                                                internal_id).first()
    if pupil == None:
        abort(400, message='This pupil does not exist!')
    authorization = db.session.query(PupilAuthorization).filter(PupilAuthorization.pupil_id == 
                                                internal_id,
                                                PupilAuthorization.origin_authorization == auth_id).first()
    if authorization == None:
        abort(400, message='This pupil authorization does not exist!')
    db.session.delete(authorization)
    db.session.commit()
    return pupil

#- PATCH PUPIL AUTHORIZATION FILE
#################################

# @pupil_authorization_api.route('/api/authorization/<authorization_id>/<pupil_id>/file', methods=['PATCH'])
# @pupil_authorization_api.input(ApiFileSchema, location='files')
# @pupil_authorization_api.output(pupil_schema)
# @pupil_authorization_api.doc(security='ApiKeyAuth',tags=['Pupil Authorizations'], summary='PATCH-POST a file to document a given pupil authorization')
# @token_required
# def upload_authorization_file(current_user, authorization_id, pupil_id, files_data):
#     authorization = db.session.query(PupilAuthorization).filter(PupilAuthorization.authorization_id == authorization_id and PupilAuthorization.authorized_pupil == pupil_id ).first() 
#     if authorization is None:
#         return jsonify( {"message": "An authorization with this date and this student does not exist!"}), 404
#     if 'file' not in files_data:
#         abort(400, message="Keine Datei angegeben!")
       
#     file = files_data['file'] 
#     filename = str(uuid.uuid4().hex) + '.jpg'
#     file_url = app.config['UPLOAD_FOLDER'] + '/auth/' + filename
#     file.save(file_url)
#     if len(str(authorization.file_url)) > 4:
#         os.remove(str(authorization.file_url))
#     authorization.file_url = file_url
#     db.session.commit()
    
#     pupil = Pupil.query.filter_by(internal_id = pupil_id).first()
#     return pupil
   

#- PATCH PUPIL AUTHORIZATION 
#############################
@pupil_authorization_api.route('/<pupil_id>/<auth_id>', methods=['PATCH'])
@pupil_authorization_api.input(pupil_authorization_in_schema)
@pupil_authorization_api.output(pupil_schema)
@pupil_authorization_api.doc(security='ApiKeyAuth', tags=['Pupil Authorizations'], summary='Patch an authorization for a given pupil')
@token_required
def patch_pupil_authorization(current_user, pupil_id, auth_id, json_data):
    pupil_authorization = db.session.query(PupilAuthorization).filter(PupilAuthorization.origin_authorization == 
                                            auth_id, PupilAuthorization.pupil_id == pupil_id).first()
    if pupil_authorization == None:
        abort(404, message="Diese Einwilligung existiert nicht!")       
    data = json_data
    for key in data:
        match key:
            case 'comment':
                pupil_authorization.comment = data[key]
            case 'status':
                pupil_authorization.status = data[key]
    #- HACKY FIX - it should be a nullable modified_by
    pupil_authorization.created_by = current_user.name
    db.session.commit()
    pupil = Pupil.query.filter_by(internal_id = pupil_id).first()
    return pupil

#- PATCH FILE TO PUPIL AUTHORIZATION
####################################
@pupil_authorization_api.route('/<pupil_id>/<origin_auth_id>/file', methods=['PATCH'])
@pupil_authorization_api.input(ApiFileSchema, location='files')
@pupil_authorization_api.output(pupil_schema)
@pupil_authorization_api.doc(security='ApiKeyAuth', tags=['Pupil Authorizations'], summary='PATCH-POST a file to document a given pupil authorization')
@token_required
def upload_pupil_authorization_file(current_user, pupil_id, origin_auth_id, files_data):
    pupil_authorization = db.session.query(PupilAuthorization).filter(PupilAuthorization.origin_authorization == 
                                            origin_auth_id, PupilAuthorization.pupil_id == pupil_id).first()
    pupil = Pupil.query.filter_by(internal_id = pupil_id).first()
    if pupil_authorization == None:
        abort(404, message="Diese Einwilligung existiert nicht!")        
    if 'file' not in files_data:
        # this means the user wants to delete the file
        if len(str(pupil_authorization.file_url)) > 4:
            os.remove(str(pupil_authorization.file_url))
        return pupil
        # return jsonify({'error': 'No file attached!'}), 400
    file = files_data['file']
    filename = file.filename
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
            abort(400, message="Filetype not allowed!")
    filename = str(uuid.uuid4().hex) + '.jpg'
    file_url = current_app.config['UPLOAD_FOLDER'] + '/auth/' + filename
    file.save(file_url)
    if len(str(pupil_authorization.file_url)) > 4:
        os.remove(str(pupil_authorization.file_url))
    pupil_authorization.file_url = file_url
    #- HACKY FIX - it should be a nullable modified_by
    pupil_authorization.created_by = current_user.name
    db.session.commit()   
    return pupil

#- GET PUPIL AUTHORIZATION FILE
###############################
@pupil_authorization_api.route('/<pupil_id>/<origin_auth_id>/file', methods=['GET'])
@pupil_authorization_api.output(FileSchema, content_type='image/jpeg')
@pupil_authorization_api.doc(security='ApiKeyAuth', tags=['Pupil Authorizations'], summary='Get file of a given pupil authorization')
@token_required
def download_pupil_authorization_file(current_user, pupil_id, origin_auth_id):
    pupil_authorization = db.session.query(PupilAuthorization).filter(PupilAuthorization.origin_authorization == 
                                            origin_auth_id, PupilAuthorization.pupil_id == pupil_id).first()
    if pupil_authorization == None:
        abort(404, message="Diese Einwilligung existiert nicht!")      
    if len(str(pupil_authorization.file_url)) < 5:
        abort(404, message="Diese Einwilligung hat keine Datei!")        
    url_path = pupil_authorization.file_url
    return send_file(url_path, mimetype='image/jpg')

##- TO-DO: REST OF AUTHORIZATION AND PUPIL AUTHORIZATION ENDPOINTS

#- DELETE PUPIL AUTHORIZATION FILE
@pupil_authorization_api.route('/<pupil_id>/<auth_id>/file', methods=['DELETE'])
@pupil_authorization_api.output(pupil_schema)
@pupil_authorization_api.doc(security='ApiKeyAuth', tags=['Pupil Authorizations'], summary='Delete file of a given pupil authorization')
@token_required
def delete_pupil_authorization_file(current_user, pupil_id, auth_id):
    pupil = db.session.query(Pupil).filter(Pupil.internal_id == 
                                                pupil_id).first()
    pupil_authorization = db.session.query(PupilAuthorization).filter(PupilAuthorization.origin_authorization == 
                                            auth_id, PupilAuthorization.pupil_id == pupil_id).first()
    if pupil_authorization == None:
        abort(404, message="Diese Einwilligung existiert nicht!")
    if len(str(pupil_authorization.file_url)) < 5:
        pupil_authorization.file_url = None
        abort(404, message="Diese Einwilligung hat keine Datei!")    
    if len(str(pupil.avatar_url)) > 4:
        os.remove(str(pupil_authorization.file_url))
    pupil_authorization.file_url = None
    log_datetime = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    user = current_user.name
    endpoint = request.method + ': ' + request.path
    payload = 'none'
    new_log_entry = LogEntry(datetime= log_datetime, user=user, endpoint=endpoint, payload=payload)
    db.session.add(new_log_entry)
    db.session.commit()   
    return pupil
