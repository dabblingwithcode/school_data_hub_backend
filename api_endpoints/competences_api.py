from apiflask import APIBlueprint, abort
from flask import jsonify
from sqlalchemy import func
from app import db
from auth_middleware import token_required
from models.competence import Competence
from schemas.competence_schemas import *

competence_api = APIBlueprint('competence_api', __name__, url_prefix='/api/competence')

#- GET COMPETENCES
##################
@competence_api.route('/all', methods=['GET'])
@competence_api.doc(security='ApiKeyAuth', tags=['Competence'], summary='Get competence list as a JSON tree', deprecated=True)
@token_required
def get_competences(current_user):
    if not current_user:
        abort(404, message='Bitte erneut einloggen!')
    root = {
        "parent_competence": "",
        "competence_id": 0,
        "competence_name": "competences",
        "competence_level": "",
        "subcompetences": [],
    }
    dict = {0: root}
    all_competences = Competence.query.all()
    for item in all_competences:
        dict[item.competence_id] = current = {
            "competence_id": item.competence_id,
            "parent_competence": item.parent_competence,
            "competence_name": item.competence_name,
            "competence_level": item.competence_level,
            "subcompetences": [],
        }
        # Adds actual category to the subcategories list of the parent
        parent = dict.get(item.parent_competence, root)
        parent["subcompetences"].append(current)

    return jsonify(root)


#- GET COMPETENCES FLAT
#######################
@competence_api.route('/all/flat', methods=['GET'])
@competence_api.output(competences_flat_schema, 200)
@competence_api.doc(security='ApiKeyAuth', tags=['Competence'], summary='Get competence list as a flat JSON')
@token_required
def get_flat_competences(current_user):
    if not current_user:
        abort(404, message='Bitte erneut einloggen!')
    all_competences = Competence.query.all()
    if all_competences == None:
        return jsonify({'error': 'No competences found!'})
    result = competences_flat_schema.dump(all_competences)
    return jsonify(result)    

#- POST NEW COMPETENCE
######################
@competence_api.route('/new', methods=['POST'])
@competence_api.input(competence_flat_schema)
@competence_api.output(competence_flat_schema)
@competence_api.doc(security='ApiKeyAuth', tags=['Competence'], summary='Post new competence')
@token_required
def post_new_competence(current_user, json_data):
    data = json_data
    competence_name = data['competence_name']
    parent_competence = data['parent_competence']
    competence_level = data['competence_level']
    indicators = data['indicators']
    max_id = db.session.query(func.max(Competence.competence_id)).scalar()
    print('max_id: ' + str(max_id))
    if max_id == None:
        max_id = 0
    new_competence = Competence( competence_id=max_id + 1, parent_competence=parent_competence,
                                competence_name=competence_name, competence_level=competence_level, indicators=indicators)
    db.session.add(new_competence)
    db.session.commit()
    return new_competence # competences_flat_schema.jsonify([new_competence])

#- PATCH COMPETENCE
###################
@competence_api.route('/<competence_id>/patch', methods=['PATCH'])
@competence_api.input(competence_flat_schema)
@competence_api.output(competence_flat_schema)
@competence_api.doc(security='ApiKeyAuth', tags=['Competence'], summary='Patch new competence')
@token_required
def patch_competence(current_user, competence_id, json_data):
    competence = Competence.query.filter_by(competence_id = competence_id).first()
    if competence == None:
        abort(400, message="Diese Kompetenz existiert nicht!")
    data = json_data
    
    for key in data:
        match key:
            case 'parent_competence':
                competence.parent_competence = data[key]
            case 'competence_name':
                competence.competence_name = data[key]
            case 'competence_level':
                competence.competence_level = data[key]
            case 'indicators':
                competence.indicators = data[key]

    db.session.commit()
    return competence # competence_flat_schema.jsonify(competence)

#- DELETE COMPETENCE
####################
@competence_api.delete('/<competence_id>/delete')
@competence_api.doc(security='ApiKeyAuth', tags=['Competence'], summary='Delete competence')
@token_required
def delete_competence(current_user, competence_id):
    competence = Competence.query.filter_by(competence_id = competence_id).first()
    if competence == None:
        abort(400, message="Diese Kompetenz existiert nicht!")
    db.session.delete(competence)
    db.session.commit()
    return jsonify({'message': 'Kompetenz erfolgreich gelöscht!'})
