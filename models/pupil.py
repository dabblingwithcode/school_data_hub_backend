from models.shared import db

class Pupil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    internal_id = db.Column(db.Integer, nullable=False, unique=True)
    contact = db.Column(db.String(50), nullable=True, unique=True)
    parents_contact = db.Column(db.String(50), nullable=True, unique=False)
    credit = db.Column(db.Integer, default = 0)
    credit_earned = db.Column(db.Integer, default = 0)
    ogs = db.Column(db.Boolean)
    pick_up_time = db.Column(db.String(5), nullable = True)
    ogs_info = db.Column(db.String(50), nullable=True)
    #- TO-DO: In order to keep track of individual development plan history, this should be a list of objects
    #-         with date, reason and created_by
    individual_development_plan = db.Column(db.Integer, default = 0)
    five_years = db.Column(db.String(2), nullable = True)
    communication_pupil = db.Column(db.String(8), nullable=True)
    communication_tutor1 = db.Column(db.String(8), nullable=True)
    communication_tutor2 = db.Column(db.String(8), nullable=True)
    preschool_revision = db.Column(db.Integer, default = 0)
    avatar_url = db.Column(db.String(50), unique=True, nullable = True)
    special_information = db.Column(db.String(200), nullable=True)

    #- RELATIONSHIPS ONE-TO-MANY
    pupil_missed_classes = db.relationship('MissedClass', back_populates='missed_pupil',
                                         cascade="all, delete-orphan")
    pupil_admonitions = db.relationship('Admonition', back_populates='admonished_pupil',
                                       cascade="all, delete-orphan")
    #- TO-DO: DOUBLE CHECK DELETE ORPHAN
    pupil_goals = db.relationship('PupilGoal', back_populates='pupil',
                                 cascade="all, delete-orphan") 
    competence_goals = db.relationship('CompetenceGoal', back_populates='pupil',
                                cascade='all, delete-orphan')
    pupil_category_statuses = db.relationship('PupilCategoryStatus', back_populates='pupil',
                                            cascade="all, delete-orphan")
    pupil_workbooks = db.relationship('PupilWorkbook', back_populates='pupil',
                                      cascade="all, delete-orphan")
    pupil_books = db.relationship('PupilBook', back_populates='pupil',
                                      cascade="all, delete-orphan")
    pupil_lists = db.relationship('PupilList', back_populates='listed_pupil',
                                 cascade="all, delete-orphan")
    competence_checks = db.relationship('CompetenceCheck', back_populates='pupil',
                                        cascade="all, delete-orphan")
    competence_reports = db.relationship('CompetenceReport', back_populates='pupil',
                                        cascade="all, delete-orphan")
    authorizations = db.relationship('PupilAuthorization', back_populates='pupil',
                                        cascade="all, delete-orphan")
    credit_history_logs = db.relationship('CreditHistoryLog', back_populates = 'pupil',
                                        cascade="all, delete-orphan")
    def __init__(self, internal_id, contact, parents_contact, credit, credit_earned, ogs, pick_up_time, ogs_info, individual_development_plan,
                 five_years, communication_pupil, communication_tutor1,
                 communication_tutor2, preschool_revision, avatar_url, special_information):
        self.internal_id = internal_id
        self.contact = contact
        self.parents_contact = parents_contact
        self.credit = credit
        self.credit_earned = credit_earned
        self.ogs = ogs
        self.pick_up_time = pick_up_time
        self.ogs_info = ogs_info
        self.individual_development_plan = individual_development_plan
        self.five_years = five_years
        self.communication_pupil = communication_pupil
        self.communication_tutor1 = communication_tutor1
        self.communication_tutor2 = communication_tutor2
        self.preschool_revision = preschool_revision
        self.avatar_url = avatar_url
        self.special_information = special_information

class CreditHistoryLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operation = db.Column(db.Integer, nullable = False)
    created_by = db.Column(db.String(20),nullable = False)
    created_at = db.Column(db.Date, nullable = False)
    credit = db.Column(db.Integer, nullable = True)

    #- RELATIONSHIP TO PUPIL MANY-TO-ONE
    pupil_id = db.Column('pupil_id', db.Integer, db.ForeignKey('pupil.internal_id'))
    pupil = db.relationship('Pupil', back_populates='credit_history_logs')
    def __init__(self, pupil_id, operation, created_by, created_at, credit):
        self.pupil_id = pupil_id
        self.operation = operation
        self.created_by = created_by
        self.created_at = created_at
        self.credit = credit


      