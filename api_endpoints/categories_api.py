from apiflask import APIBlueprint, abort
from flask import jsonify
from app import db
from auth_middleware import token_required
from models.category import GoalCategory
from schemas.goal_schemas import *

goal_category_api = APIBlueprint('goal_categories_api', __name__, url_prefix='/api/goal_categories')

#- GET CATEGORIES 
###############################

@goal_category_api.route('/all', methods=['GET'])
@goal_category_api.doc(security='ApiKeyAuth', tags=['Goal Categories'], summary='Get goal categories')
@token_required
def get_categories(current_user):
    if not current_user:
        abort(404, message='Bitte erneut einloggen!')
    root = {
        "category_id": 0,
        "category_name": "development_goal_categories",
        "subcategories": [],
    }
    dict = {0: root}
    all_categories = GoalCategory.query.all()
    if all_categories == []:
        abort(404, message="No categories found!")
    for item in all_categories:
        dict[item.category_id] = current = {
            "category_id": item.category_id,
            "parent_category": item.parent_category,
            "category_name": item.category_name,
            "subcategories": [],
        }
        # Adds actual category to the subcategories list of the parent
        parent = dict.get(item.parent_category, root)
        parent["subcategories"].append(current)

    return jsonify(root)

#- GET CATEGORIES FLAT
######################

@goal_category_api.route('/all/flat', methods=['GET'])
@goal_category_api.output(goal_categories_flat_schema)
@goal_category_api.doc(security='ApiKeyAuth', tags=['Goal Categories'], summary='Get goal categories in flat JSON')

@token_required
def get_flat_categories(current_user):
    if not current_user:
        abort(404, message='Bitte erneut einloggen!')
    all_categories = GoalCategory.query.all()
    if all_categories == None:
        return jsonify({'error': 'No categories found!'})
    result = goal_categories_flat_schema.dump(all_categories)
    return jsonify(result)    


#! TODO: Add new category