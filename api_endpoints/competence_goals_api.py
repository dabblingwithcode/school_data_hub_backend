from datetime import datetime
import uuid
from apiflask import APIBlueprint, abort
from flask import jsonify
from schemas.competence_schemas import *
from schemas.pupil_schemas import *
from models.pupil import Pupil
from models.competence import Competence, CompetenceGoal

from app import db
from auth_middleware import token_required

competence_goal_api = APIBlueprint('competence_goal_api', __name__, url_prefix='/api/competence_goals')

#- POST COMPETENCE GOAL
#######################
@competence_goal_api.post('/new/<internal_id>')
@competence_goal_api.input(competence_goal_in_schema)
@competence_goal_api.output(pupil_schema, 200)
@competence_goal_api.doc(security='ApiKeyAuth', tags=['Competence Goals'], summary='Post a goal associated with a competence')
@token_required
def post_competence_goal(current_user, internal_id, json_data):
    pupil = Pupil.query.filter_by(internal_id = internal_id).first()
    if pupil == None:
        abort(400, message="Diese/r Schüler/in existiert nicht!")
    data = json_data
    pupil_id = pupil.internal_id
    competence_id = data['competence_id']
    competence = Competence.query.filter_by(competence_id = competence_id).first()
    if competence == None:
        abort(400, message="Diese Kompetenz existiert nicht!")
    competence_goal_id = str(uuid.uuid4().hex)
    created_by = current_user.name
    created_at = datetime.now().date() 
    achieved = None
    achieved_at = None
    description = data['description']
    strategies = data['strategies']
    new_goal = CompetenceGoal(competence_goal_id=competence_goal_id, created_by=created_by, modified_by=None, created_at=created_at, achieved=achieved,
                         achieved_at=achieved_at, description=description, strategies=strategies, pupil_id=pupil_id, competence_id=competence_id)
    db.session.add(new_goal)
    db.session.commit()
    return pupil

#- PATCH COMPETENCE GOAL
########################
@competence_goal_api.route('/<goal_id>', methods=['PATCH'])
@competence_goal_api.input(competence_goal_in_schema)
@competence_goal_api.output(competence_goal_out_schema)
@competence_goal_api.doc(security='ApiKeyAuth', tags=['Competence Goals'], summary='Patch a goal associated with a competence')
@token_required
def patch_competence_goal(current_user, goal_id, json_data):
    competence_goal = CompetenceGoal.query.filter_by(competence_goal_id = goal_id).first()
    if competence_goal == None:
        abort(400, message="Diese Kompetenz existiert nicht!")        
    data = json_data
    competence_goal.modified_by = current_user.name
    for key in data:
        match key:
            case 'created_at':
                competence_goal.created_at = data[key]
            case 'achieved':
                competence_goal.achieved = data[key]
            case 'achieved_at':
                competence_goal.achieved_at = data[key]
            case 'description':
                competence_goal.description = data[key]
            case 'strategies':
                competence_goal.strategies = data[key]
    db.session.commit()
    return competence_goal

#- DELETE COMPETENCE GOAL
#########################
@competence_goal_api.delete('/<goal_id>/delete')
@competence_goal_api.doc(security='ApiKeyAuth', tags=['Competence Goals'], summary='Delete a goal associated with a competence')
@token_required
def delete_competence_goal(current_user, goal_id):
    competence_goal = CompetenceGoal.query.filter_by(competence_goal_id = goal_id).first()
    if competence_goal == None:
        abort(400, message="Diese Kompetenz existiert nicht!")
    db.session.delete(competence_goal)
    db.session.commit()
    return jsonify({'message': 'Kompetenz erfolgreich gelöscht!'})
