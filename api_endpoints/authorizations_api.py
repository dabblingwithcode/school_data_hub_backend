import uuid
from apiflask import APIBlueprint, abort
from flask import jsonify
from app import db
from auth_middleware import token_required
from models.pupil import Pupil
from models.authorization import Authorization, PupilAuthorization
from schemas.authorization_schemas import *
from schemas.pupil_schemas import *

authorization_api = APIBlueprint('authorizations_api', __name__, url_prefix='/api/authorizations')

#- POST AUTHORIZATION WITH ALL PUPILS
#####################################
@authorization_api.route('/new/all', methods=['POST'])
@authorization_api.input(authorization_in_schema)
@authorization_api.output(pupils_schema)
@authorization_api.doc(security='ApiKeyAuth', tags=['Authorizations'], summary='Post an authorization including ALL pupils in the database')
@token_required
def add_authorization_all(current_user, json_data):
    authorization_id = str(uuid.uuid4().hex)
    authorization_name = json_data['authorization_name']
    authorization_description = json_data['authorization_description']
    existing_authorization = Authorization.query.filter_by(authorization_name = authorization_name).first()
    if existing_authorization:
        return jsonify({'message': 'Diese Einwilligung existiert schon!'}), 400
    user_name = current_user.name
    new_authorization = Authorization( authorization_id,  authorization_name,  authorization_description, user_name)
    db.session.add(new_authorization)
    all_pupils = Pupil.query.all()
    for item in all_pupils:
        origin_authorization = authorization_id
        pupil_id = item.internal_id
        status = None
        comment = None
        #- HACKY FIX - this should be a nullable modified_by
        created_by = ''
        new_pupil_authorization = PupilAuthorization(status=status, comment=comment, created_by=user_name, file_url=None, origin_authorization=origin_authorization, pupil_id=pupil_id)
        db.session.add(new_pupil_authorization)
    db.session.commit()    
    return all_pupils

#- POST AUTHORIZATION WITH LIST OF PUPILS
#########################################
@authorization_api.route('/new/list', methods=['POST'])
@authorization_api.input(authorization_in_group_schema)
@authorization_api.output(pupils_schema)
@authorization_api.doc(security='ApiKeyAuth', tags=['Authorizations'], summary='Post an authorization including pupils from an array')
@token_required
def add_authorization_group(current_user, json_data):
    data = json_data
    authorization_name = data['authorization_name']
    authorization_description = data['authorization_description']
    existing_authorization = Authorization.query.filter_by(authorization_name = authorization_name).first()
    if existing_authorization:
        return jsonify({'message': 'Diese Einwilligung existiert schon!'}), 400
    authorization_id = str(uuid.uuid4().hex)
    created_by = current_user.name
    new_authorization = Authorization( authorization_id,  authorization_name,  authorization_description, created_by)
    db.session.add(new_authorization)
    pupil_id_list = data['pupils']
        #-We have to create the list to populate it with pupils.
    #-This is why it is created even if pupils are wrong and the list remains empty. 
    pupils = []
    for item in pupil_id_list:
        pupil = Pupil.query.filter_by(internal_id = item).first()
        if pupil is not None:
            pupils.append(pupil)
            origin_authorization = authorization_id
            pupil_id = item
            status = None
            comment = None
            #- HACKY FIX - this should be a nullable modified_by
            created_by = ''
            new_pupil_authorization = PupilAuthorization(origin_authorization=origin_authorization, pupil_id=pupil_id, status=status, comment=comment, created_by=created_by, file_url=None)
            db.session.add(new_pupil_authorization)
    db.session.commit()    
    return pupils

#- GET ALL AUTHORIZATIONS
#########################
@authorization_api.route('/all', methods=['GET'])
@authorization_api.output(authorizations_schema)
@authorization_api.doc(security='ApiKeyAuth', tags=['Authorizations'], summary='Get all authorizations with authorized pupils')
@token_required
def get_authorizations(current_user):
    all_authorizations = Authorization.query.all()
    if all_authorizations == []:
        return jsonify({'error': 'There are no authorizations!'})
    result = authorizations_schema.dump(all_authorizations)
    return jsonify(result)

#- GET ALL AUTHORIZATIONS FLAT
##############################
@authorization_api.route('/all/flat', methods=['GET'])
@authorization_api.output(authorizations_flat_schema)
@authorization_api.doc(security='ApiKeyAuth', tags=['Authorizations'], summary='Get all authorizations')
@token_required
def get_authorizations_flat(current_user):
    all_authorizations = Authorization.query.all()
    if all_authorizations == []:
        return jsonify({'error': 'There are no authorizations!'})
    result = authorizations_flat_schema.dump(all_authorizations)
    return jsonify(result)

#-DELETE AUTHORIZATION 
######################
@authorization_api.route('/<auth_id>', methods=['DELETE'])
@authorization_api.doc(security='ApiKeyAuth', tags=['Authorizations'], summary='Delete an authorization')
@token_required
def delete_authorization(current_user, auth_id):
    if not current_user.admin:
        abort(401, message='Keine Berechtigung!')      
    authorization = db.session.query(Authorization).filter(Authorization.authorization_id == 
                                            auth_id).first()
    if authorization == None:
        abort(404, message="This authorization does not exist!")        
    db.session.delete(authorization)              
    db.session.commit()
    abort(200, message="The authorization was deleted!")

#- PATCH AUTHORIZATION
######################
@authorization_api.route('/<auth_id>', methods=['PATCH'])
@authorization_api.input(authorization_in_schema)
@authorization_api.output(authorization_schema)
@authorization_api.doc(security='ApiKeyAuth', tags=['Authorizations'], summary='Patch an authorization')
@token_required
def patch_authorization(current_user, auth_id, json_data):
    if not current_user.admin:
        abort(401, message='Keine Berechtigung!')      
    data = json_data
    existing_authorization = Authorization.query.filter_by(authorization_id = auth_id).first()
    if existing_authorization is None:
        abort(404, message="Diese Einwilligung existiert nicht!")        
    authorization_name = data['authorization_name']
    authorization_description = data['authorization_description']
    existing_authorization.authorization_name = authorization_name
    existing_authorization.authorization_description = authorization_description
    db.session.commit()
    return existing_authorization
    
         