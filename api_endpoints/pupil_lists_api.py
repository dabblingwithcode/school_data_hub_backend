from apiflask import APIBlueprint, abort
from flask import jsonify
from app import db
from auth_middleware import token_required
from schemas.school_list_schemas import *
from schemas.pupil_schemas import *
from models.pupil import Pupil
from models.school_list import PupilList, SchoolList

pupil_list_api = APIBlueprint('pupil_list_api', __name__, url_prefix='/api/pupil_lists')

#- PATCH a PUPILLIST
####################
@pupil_list_api.route('/<pupil_id>/<list_id>', methods=['PATCH'])
@pupil_list_api.input(pupil_list_patch_schema)
@pupil_list_api.output(pupil_schema)
@pupil_list_api.doc(security='ApiKeyAuth', tags=['Pupil Lists'], summary='Patch a pupil list entry')
@token_required
def patch_pupil_list(current_user, pupil_id, list_id, json_data):
    pupil = Pupil.query.filter_by(internal_id = pupil_id).first()
    pupil_list = PupilList.query.filter_by(origin_list = list_id, listed_pupil_id = pupil_id).first()
    if pupil_list is None:
        abort(404, message="Der Listeneintrag existiert nicht!")
    data = json_data
    for key in data:
        match key:
            case 'pupil_list_comment':
                pupil_list.pupil_list_comment = data[key]
            case 'pupil_list_status':
                pupil_list.pupil_list_status = data[key]
            case 'pupil_list_entry_by':
                pupil_list.pupil_list_entry_by = data[key]
    db.session.commit()
    return pupil

#- DELETE PUPILS FROM SCHOOL LIST
#################################
@pupil_list_api.route('/<list_id>/delete_pupils', methods=['POST'])
@pupil_list_api.input(pupil_id_list_schema)
@pupil_list_api.output(pupils_schema)
@pupil_list_api.doc(security='ApiKeyAuth', tags=['Pupil Lists'], summary='Delete pupil entries from list')
@token_required
def delete_pupil_list(current_user, list_id, json_data):
    data = json_data
    internal_id_list = data['pupils']
    if current_user.name != SchoolList.query.filter_by(list_id = list_id).first().created_by:
        abort(401, message="Keine Berechtigung!")
    if internal_id_list == []:
        abort(404, message="Keine Schueler angegeben!")
    updated_pupils = []
    for item in internal_id_list:
        pupil = Pupil.query.filter_by(internal_id = item).first()        
        if pupil != None:
            updated_pupils.append(pupil)
            pupil_list = PupilList.query.filter_by(origin_list= list_id, listed_pupil_id= item).first()
            if pupil_list != None:
                db.session.delete(pupil_list)
    db.session.commit()
    result = pupils_schema.dump(updated_pupils)
    return jsonify(result)