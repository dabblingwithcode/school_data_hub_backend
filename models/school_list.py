from models.schoolday import *

class SchoolList(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    list_id = db.Column(db.String(50), unique=True)
    list_name = db.Column(db.String(20), nullable = False)
    list_description = db.Column(db.String(100), nullable=False)
    created_by = db.Column(db.String(5), nullable = False)
    visibility = db.Column(db.String(5), nullable = False)

    #- RELATIONSHIP TO PUPILS ONE-TO-MANY over PUPIL LIST
    pupils_in_list = db.relationship('PupilList', back_populates='pupil_in_list',
                                   cascade="all, delete-orphan")
    def __init__(self, list_id, list_name, list_description, created_by, visibility):
        self.list_id = list_id
        self.list_name = list_name
        self.list_description = list_description
        self.created_by = created_by
        self.visibility = visibility

class PupilList(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    pupil_list_status = db.Column(db.Boolean)
    pupil_list_comment = db.Column(db.String(30))
    pupil_list_entry_by = db.Column(db.String(20))

    #- RELATIONSHIP TO SCHOOL LIST MANY-TO-ONE
    origin_list = db.Column(db.String(50), db.ForeignKey('school_list.list_id'))
    pupil_in_list = db.relationship('SchoolList', back_populates='pupils_in_list')

    #- RELATIONSHIP TO PUPIL MANY-TO-ONE
    listed_pupil_id = db.Column(db.Integer, db.ForeignKey('pupil.internal_id'))
    listed_pupil = db.relationship('Pupil', back_populates='pupil_lists')
    def __init__(self, pupil_list_status, pupil_list_comment, pupil_list_entry_by,
                 origin_list, listed_pupil_id):
        self.origin_list = origin_list
        self.listed_pupil_id = listed_pupil_id
        self.pupil_list_status = pupil_list_status
        self.pupil_list_comment = pupil_list_comment
        self.pupil_list_entry_by = pupil_list_entry_by    