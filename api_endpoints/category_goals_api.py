from datetime import datetime
import uuid
from apiflask import APIBlueprint, abort
from flask import jsonify, request
from app import db
from auth_middleware import token_required
from models.pupil import Pupil
from models.category import GoalCategory, PupilGoal, GoalCheck
from schemas.goal_schemas import *
from schemas.pupil_schemas import *

category_goals_api = APIBlueprint('category_goals_api', __name__, url_prefix='/api/category_goals')

#- POST GOAL
############
@category_goals_api.route('/<internal_id>/new', methods=['POST'])
@category_goals_api.input(pupil_goal_in_schema)
@category_goals_api.output(pupil_schema)
@category_goals_api.doc(security='ApiKeyAuth', tags=['Goals'], summary='Post a goal for a given gategory')
@token_required
def add_goal(current_user, internal_id, json_data):
    data = json_data
    pupil = Pupil.query.filter_by(internal_id = internal_id).first()
    if pupil == None:
        abort(404, message='Schüler/Schülerin existiert nicht!')
    pupil_id = pupil.internal_id
    goal_category_id = data['goal_category_id']
    goal_category = db.session.query(GoalCategory).filter_by(category_id = goal_category_id).scalar()
    if goal_category == None:
        abort(404, message='Diese Kategorie existiert nicht!')
    goal_id = str(uuid.uuid4().hex)
    created_by = current_user.name
    created_at = data['created_at'] 
    #created_at_datetime = datetime.strptime(created_at, '%Y-%m-%d').date() 
    achieved = data['achieved']
    achieved_at = data['achieved_at']
    # if achieved_at:
    #     achieved_at = datetime.strptime(achieved_at, '%Y-%m-%d').date()
    # else:
    #     achieved_at = None
    description = data['description']
    strategies = data['strategies']
    new_goal = PupilGoal(pupil_id, goal_category_id, goal_id, created_by, created_at, achieved,
                         achieved_at, description, strategies)
    db.session.add(new_goal)
    db.session.commit()
    return pupil

#- PATCH GOAL 
#############
@category_goals_api.route('/<goal_id>', methods=['PATCH'])
@category_goals_api.input(pupil_goal_in_schema)
@category_goals_api.output(pupil_goal_schema)
@category_goals_api.doc(security='ApiKeyAuth', tags=['Goals'], summary='Patch a goal for a given gategory from a given pupil')
@token_required
def put_goal(current_user, goal_id, json_data):
    goal = PupilGoal.query.filter_by(goal_id = goal_id).first()
    if goal == None:
        return jsonify({'error': 'This goal does not exist!'})
    data = json_data
    for key in data:
        match key:
            case 'created_at':
                goal.created_at = data[key]
            case 'achieved':
                goal.achieved = data[key]
            case 'achieved_at':
                goal.achieved_at = data[key] # datetime.strptime(data[key], '%Y-%m-%d').date() 
            case 'description':
                goal.description = data[key]
            case 'strategies':
                goal.strategies = data[key]
    db.session.commit()
    return goal

#- DELETE GOAL
##############
@category_goals_api.delete('/<goal_id>/delete')
@category_goals_api.output(pupil_schema)
@category_goals_api.doc(security='ApiKeyAuth', tags=['Goals'], summary='Delete a goal for a given gategory from a given pupil')
@token_required
def delete_goal(current_user, goal_id):
    goal = PupilGoal.query.filter_by(goal_id = goal_id).first()
    if goal == None:
        abort(404, message='This goal does not exist!')
    pupil = Pupil.query.filter_by(internal_id = goal.pupil_id).first()
    db.session.delete(goal)
    db.session.commit()
    return pupil

#- POST GOAL CHECK 
##################
@category_goals_api.route('/<goal_id>/check/new', methods=['POST'])
@category_goals_api.input(goal_check_in_schema)
@category_goals_api.output(pupil_schema)
@category_goals_api.doc(security='ApiKeyAuth', tags=['Goal Checks'], summary='Post a check for a given goal from a given pupil')
@token_required
def add_goalcheck(current_user, goal_id, json_data):
    this_goal = PupilGoal.query.filter_by(goal_id = goal_id).first()
    if this_goal == None:
        abort(404, message='Dieses Ziel existiert nicht!')
    pupil = Pupil.query.filter_by(internal_id = this_goal.pupil_id).first()   
    this_goal_id = goal_id
    check_id = str(uuid.uuid4().hex)
    created_by = current_user.name
    created_at = datetime.now().date()
    comment = json_data['comment']
    new_goalcheck = GoalCheck(this_goal_id, check_id, created_by, created_at, comment)
    db.session.add(new_goalcheck)
    db.session.commit()
    return pupil

#- PATCH GOAL CHECK 
###################
@category_goals_api.route('/<goal_id>/check/<check_id>', methods=['PATCH'])
@category_goals_api.doc(security='ApiKeyAuth', tags=['Goal Checks'], summary='Patch a check for a given goal from a given pupil')
@token_required
def patch_goalcheck(current_user, goal_id, check_id):
    goal_check = GoalCheck.query.filter_by(goal_id = goal_id, id = check_id).first()
    if goal_check == None:
        return jsonify({'error': 'This goal check does not exist!'})
    data = request.get_json()
    for key in data:
        match key:
            case 'created_at':
                goal_check.created_at = datetime.strptime(data[key], '%Y-%m-%d').date()
            case 'comment':
                goal_check.comment = data[key]
    db.session.commit()
    return goalcheck_schema.jsonify(goal_check)
