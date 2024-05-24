from models.shared import db

class Competence(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    competence_id = db.Column(db.Integer, unique=True, nullable = False)
    parent_competence = db.Column(db.Integer, nullable = True)
    competence_name = db.Column(db.String(100), nullable = False)
    competence_level = db.Column(db.String(10), nullable = True)
    indicators = db.Column(db.String(200), nullable = True)

    #- RELATIONSHIP TO CHECKS ONE-TO-MANY
    competence_checks = db.relationship('CompetenceCheck', back_populates='competence_check')
    #- RELATIONSHIP TO COMPETENCE GOALS ONE-TO-MANY
    competence_goals = db.relationship('CompetenceGoal', back_populates='competence')

    def __init__(self, competence_id, parent_competence, competence_name, competence_level, indicators):
        self.competence_id = competence_id
        self.parent_competence = parent_competence
        self.competence_name = competence_name
        self.competence_level = competence_level
        self.indicators = indicators

class CompetenceGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    competence_goal_id = db.Column(db.String(50), unique=True)
    created_by = db.Column(db.String(20),nullable = False)
    modifed_by = db.Column(db.String(20),nullable = True)
    created_at = db.Column(db.Date, nullable = False)
    achieved = db.Column(db.Integer, nullable = True)
    achieved_at = db.Column(db.Date, nullable = True)
    description = db.Column(db.String(200), nullable = False)
    strategies = db.Column(db.String(500))
    #- RELATIONSHIP TO PUPIL MANY-TO-ONE
    pupil_id = db.Column(db.Integer, db.ForeignKey('pupil.internal_id'))
    pupil = db.relationship('Pupil', back_populates='competence_goals')
    #- RELATIONSHIP TO COMPETENCE MANY-TO-ONE
    competence_id = db.Column('competence_id', db.Integer,
                                 db.ForeignKey('competence.id'))
    competence = db.relationship('Competence', back_populates='competence_goals')

    def __init__(self, competence_goal_id, created_by, modified_by, created_at, achieved, achieved_at, description, strategies,
                 pupil_id, competence_id):
        self.competence_goal_id = competence_goal_id
        self.created_by = created_by
        self.modified_by = modified_by
        self.created_at = created_at
        self.achieved = achieved
        self.achieved_at = achieved_at
        self.description = description
        self.strategies = strategies
        self.pupil_id = pupil_id
        self.competence_id = competence_id

class CompetenceCheck(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    check_id = db.Column(db.String(50), unique=True)
    is_report = db.Column(db.Boolean)
    created_by = db.Column(db.String(20),nullable = False)
    created_at = db.Column(db.Date, nullable = False)
    competence_status = db.Column(db.Integer, nullable = False)
    comment = db.Column(db.String(200), nullable = False)

    #- RELATIONSHIP TO COMPETENCE CHECK FILES ONE-TO-MANY
    competence_check_files = db.relationship('CompetenceCheckFile', back_populates='competence_check',
                                        cascade="all, delete-orphan")
    #- RELATIONSHIP TO PUPIL MANY-TO-ONE
    pupil_id = db.Column(db.Integer, db.ForeignKey('pupil.internal_id'))
    pupil = db.relationship('Pupil', back_populates='competence_checks')

    #- RELATIONSHIP TO COMPETENCE MANY-TO-ONE
    competence_id = db.Column(db.Integer, db.ForeignKey('competence.competence_id'))
    competence_check = db.relationship('Competence', back_populates='competence_checks')

    #- RELATIONSHIP TO COMPETENCE REPORT MANY-TO-ONE
    report_id = db.Column(db.String(50), db.ForeignKey('competence_report.report_id'), nullable = True)
    competence_report = db.relationship('CompetenceReport', back_populates='competence_checks')

    def __init__(self, check_id, is_report, created_by, created_at, competence_status, comment, pupil_id, competence_id, report_id):
        self.check_id = check_id
        self.is_report = is_report
        self.created_by = created_by
        self.created_at = created_at
        self.competence_status = competence_status
        self.comment = comment
        self.pupil_id = pupil_id
        self.competence_id = competence_id
        self.report_id = report_id

class CompetenceCheckFile(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    file_id = db.Column(db.String(50), unique=True, nullable = False)
    file_url = db.Column(db.String(50), unique=True, nullable = False)

    #- RELATIONSHIP TO COMPETENCE CHECK MANY-TO-ONE
    check_id = db.Column(db.String(50), db.ForeignKey('competence_check.check_id'))
    competence_check = db.relationship('CompetenceCheck', back_populates='competence_check_files')

    def __init__(self, check_id, file_id, file_url):
        self.check_id = check_id
        self.file_id = file_id
        self.file_url = file_url

class CompetenceReport(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    report_id = db.Column(db.String(50), unique=True)
    created_by = db.Column(db.String(20),nullable = False)
    created_at = db.Column(db.Date, nullable = False)
    #- RELATIONSHIP TO PUPIL MANY-TO-ONE
    pupil_id = db.Column(db.Integer, db.ForeignKey('pupil.internal_id'))
    pupil = db.relationship('Pupil', back_populates='competence_reports')    
    #- RELATIONSHIP TO COMPETENCE CHECK ONE-TO-MANY
    competence_checks = db.relationship('CompetenceCheck', back_populates='competence_report',
                                        cascade='all, delete-orphan')
    
    school_semester_id = db.Column(db.Integer, db.ForeignKey('school_semester.id'))
    school_semester = db.relationship('SchoolSemester', backref='competence_reports')

    # Define a unique constraint on the combination of pupil_id and school_semester_id
    __table_args__ = (
        db.UniqueConstraint('pupil_id', 'school_semester_id', name='uq_pupil_school_semester'),
    )

    def __init__(self, report_id, created_by, created_at, pupil_id, school_semester_id):
        self.report_id = report_id
        self.created_by = created_by
        self.created_at = created_at
        self.pupil_id = pupil_id
        self.school_semester_id = school_semester_id