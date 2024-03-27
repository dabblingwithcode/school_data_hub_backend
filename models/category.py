from .schoolday import db

class PupilCategoryStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status_id = db.Column(db.String(50), unique=True)
    state = db.Column(db.String(10), nullable = False)
    created_by = db.Column(db.String(20),nullable = False)
    created_at = db.Column(db.Date, nullable = False)
    comment = db.Column(db.String(200), nullable = True)
    file_url = db.Column(db.String(50), nullable = True)

    #- RELATIONSHIP TO PUPIL MANY-TO-ONE
   
    pupil_id = db.Column('pupil_id', db.Integer, db.ForeignKey('pupil.internal_id'))
    pupil = db.relationship('Pupil', back_populates='pupil_category_statuses')

    #- RELATIONSHIP TO CATEGORY MANY-TO-ONE
    goal_category_id = db.Column('goal_category_id', db.Integer,
                                 db.ForeignKey('goal_category.id'))
    goal_category = db.relationship('GoalCategory', back_populates='category_statuses')

    def __init__(self, pupil_id, goal_category_id, status_id, state, created_by, created_at, comment, file_url):
        self.pupil_id = pupil_id
        self.goal_category_id = goal_category_id
        self.status_id = status_id
        self.state = state
        self.created_by = created_by
        self.created_at = created_at
        self.comment = comment
        self.file_url = file_url

class PupilGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.String(50), unique=True)
    created_by = db.Column(db.String(20),nullable = False)
    created_at = db.Column(db.Date, nullable = False)
    achieved = db.Column(db.Integer)
    achieved_at = db.Column(db.Date, nullable = True)
    description = db.Column(db.String(200), nullable = False)
    strategies = db.Column(db.String(500))

    #- RELATIONSHIP TO PUPIL MANY-TO-ONE
    pupil_id = db.Column(db.Integer, db.ForeignKey('pupil.internal_id'))
    pupil = db.relationship('Pupil', back_populates='pupil_goals')

    #- RELATIONSHIP TO CATEGORY MANY-TO-ONE
    goal_category_id = db.Column('goal_category_id', db.Integer,
                                 db.ForeignKey('goal_category.id'))
    goal_category = db.relationship('GoalCategory', back_populates='category_goals')

    #- RELATIONSHIP TO CHECKS ONE-TO-MANY
    goal_checks = db.relationship('GoalCheck', back_populates='goal',
                                 cascade="all, delete-orphan")

    def __init__(self, pupil_id, goal_category_id, goal_id, created_by, created_at, achieved,
                 achieved_at, description, strategies):
        self.pupil_id = pupil_id
        self.goal_category_id = goal_category_id
        self.goal_id = goal_id
        self.created_by = created_by
        self.created_at = created_at
        self.achieved = achieved
        self.achieved_at = achieved_at
        self.description = description
        self.strategies = strategies

class GoalCategory(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    category_id = db.Column(db.Integer, nullable = False)
    parent_category = db.Column(db.Integer, nullable = True)
    category_name = db.Column(db.String(200), nullable = False)

    #- RELATIONSHIP TO GOALS ONE-TO-MANY
    category_goals = db.relationship('PupilGoal', back_populates='goal_category')

    #- RELATIONSHIP TO PUPIL CATEGORY STATUS ONE-TO-MANY
    category_statuses = db.relationship('PupilCategoryStatus',
                                       back_populates='goal_category')
    
    def __init__(self, category_id, parent_category, category_name):
        self.category_id = category_id
        self.parent_category = parent_category
        self.category_name = category_name
        

class GoalCheck(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    check_id = db.Column(db.String(50), unique=True, nullable = False)
    created_by = db.Column(db.String(5), nullable = False)

    created_at = db.Column(db.Date, nullable = False)
    comment = db.Column(db.String(50), nullable = False)
    
    #- RELATIONSHIP TO PUPIL GOAL MANY-TO-ONE
    goal_id = db.Column(db.String(50), db.ForeignKey('pupil_goal.goal_id'))
    goal = db.relationship('PupilGoal', back_populates='goal_checks')

    def __init__(self, goal_id, check_id,created_by, created_at, comment):
        self.goal_id = goal_id
        self.check_id = check_id
        self.created_by = created_by
        self.created_at = created_at
        self.comment = comment