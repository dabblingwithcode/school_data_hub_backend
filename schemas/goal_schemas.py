from apiflask import Schema, fields

#- GOAL CHECK SCHEMA
#####################

class GoalCheckInSchema(Schema):
    id = fields.Integer()
    comment = fields.String()
    goal_id = fields.String()
    class Meta:
        fields = ('id','comment', 'goal_id')

goal_check_in_schema = GoalCheckInSchema()
goal_checks_in_schema = GoalCheckInSchema(many = True)

class GoalCheckSchema(Schema):
    id = fields.Integer()
    created_by = fields.String()
    created_at = fields.Date()
    comment = fields.String()
    goal_id = fields.String()
    check_id = fields.String()
    class Meta:
        fields = ('id','created_by', 'created_at', 'comment', 'goal_id', 'check_id')

goalcheck_schema = GoalCheckSchema()
goal_checks_schema = GoalCheckSchema(many = True)

class PupilGoalInSchema(Schema):
    goal_id = fields.String()
    goal_category_id = fields.Integer()
    created_by = fields.String()
    created_at = fields.Date()
    achieved = fields.Integer()
    achieved_at = fields.Date(allow_none=True)
    description = fields.String()
    strategies = fields.String()
    class Meta:
        fields = ('goal_id','goal_category_id', 'created_by', 
                  'created_at', 'achieved', 'achieved_at', 'description',
                   'strategies')

pupil_goal_in_schema = PupilGoalInSchema()
pupil_goals_in_schema = PupilGoalInSchema(many = True)

class PupilGoalSchema(Schema):
    goal_id = fields.String()
    pupil_id = fields.Integer()
    goal_category_id = fields.Integer()
    created_by = fields.String()
    created_at = fields.Date()
    achieved = fields.Integer()
    achieved_at = fields.Date(allow_none=True)
    description = fields.String()
    strategies = fields.String()
    goal_checks = fields.List(fields.Nested(GoalCheckSchema))
    class Meta:
        fields = ('goal_id', 'pupil_id', 'goal_category_id', 'created_by', 
                  'created_at', 'achieved', 'achieved_at', 'description',
                   'strategies', 'goal_checks')

pupil_goal_schema = PupilGoalSchema()
pupil_goals_schema = PupilGoalSchema(many = True)

#- PUPIL CATEGORY STATUS SCHEMA
################################

class PupilCategoryStatusInSchema(Schema):
    state = fields.String()
    comment = fields.String(allow_none=True)
    file_url = fields.String(allow_none=True)
    class Meta:
        fields = ('state', 'comment', 'file_url')    

pupil_category_status_in_schema = PupilCategoryStatusInSchema()
pupil_category_statuses_in_schema = PupilCategoryStatusInSchema(many= True)

class PupilCategoryStatusSchema(Schema):
    id = fields.Integer()
    goal_category_id = fields.Integer()
    status_id = fields.String()
    state = fields.String()
    comment = fields.String(allow_none=True)
    file_url = fields.String(allow_none=True)
    created_by = fields.String()
    created_at = fields.Date()    
    class Meta:
        fields = ('id', 'goal_category_id', 'status_id', 'state', 'comment', 'file_url', 
                  'created_by', 'created_at')    

pupil_category_status_schema = PupilCategoryStatusSchema()
pupil_category_statuses_schema = PupilCategoryStatusSchema(many= True)

#- GOAL CATEGORY SCHEMA
#######################

class GoalCategorySchema(Schema):
    category_id = fields.Integer()
    category_name = fields.String()
    category_goals = fields.List(fields.Nested(PupilGoalSchema))
    category_statuses = fields.List(fields.Nested(PupilCategoryStatusSchema))
    class Meta:
        fields = ('category_id', 'category_name', 'category_goals',
                  'category_statuses')

goal_category_schema = GoalCategorySchema()
goal_categories_schema = GoalCategorySchema(many = True)

#- GOAL CATEGORY SCHEMA FLAT
#############################

class GoalCategoryFlatSchema(Schema):
    category_id = fields.Integer()
    category_name = fields.String()
    parent_category = fields.Integer()
    class Meta:
        fields = ('category_id', 'category_name', 'parent_category')

goal_category_flat_schema = GoalCategoryFlatSchema()
goal_categories_flat_schema = GoalCategoryFlatSchema(many = True)
