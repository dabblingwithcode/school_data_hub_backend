from models.schoolday import *

class Workbook(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    isbn = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(20))
    subject = db.Column(db.String(10))
    level = db.Column(db.String(5), nullable = False)

    image_url = db.Column(db.String(50), nullable = True)

    #- RELATIONSHIP TO PUPIL WORKBOOKS ONE-TO-MANY
    working_pupils = db.relationship('PupilWorkbook', back_populates='workbook',
                                     cascade='all, delete-orphan')

    def __init__(self, isbn, name, subject, level, image_url):
        self.isbn = isbn
        self.name = name
        self.subject = subject
        self.level = level
        self.image_url = image_url

class PupilWorkbook(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    state = db.Column(db.String(10), nullable = True)
    created_by = db.Column(db.String(20),nullable = False)
    created_at = db.Column(db.Date, nullable = False)

    finished_at = db.Column(db.Date, nullable = True)

    #- RELATIONSHIP TO PUPIL MANY-TO-ONE
    pupil_id = db.Column('pupil_id', db.Integer, db.ForeignKey('pupil.internal_id'))
    pupil = db.relationship('Pupil', back_populates='pupil_workbooks')

    #- RELATIONSHIP TO WORKBOOK MANY-TO-ONE
    workbook_isbn = db.Column('isbn_id', db.Integer, db.ForeignKey('workbook.isbn'))
    workbook = db.relationship('Workbook', back_populates='working_pupils')

    def __init__(self, pupil_id, workbook_isbn, state, created_by, created_at, finished_at):
        self.pupil_id = pupil_id
        self.workbook_isbn = workbook_isbn
        self.state = state
        self.created_by = created_by
        self.created_at = created_at
        self.finished_at = finished_at