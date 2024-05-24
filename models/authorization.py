from models.shared import db

class Authorization(db.Model):    
    id = db.Column(db.Integer, primary_key = True)
    authorization_id = db.Column(db.String(50), unique=True)
    authorization_name = db.Column(db.String(20), nullable = False)
    authorization_description = db.Column(db.String(100), nullable=False)
    created_by = db.Column(db.String(5), nullable = False)

    authorized_pupils = db.relationship('PupilAuthorization', back_populates='authorized_pupil',
                                        cascade="all, delete-orphan")
    
    def __init__(self, authorization_id, authorization_name, authorization_description, created_by):
        self.authorization_id = authorization_id
        self.authorization_name = authorization_name
        self.authorization_description = authorization_description
        self.created_by = created_by

class PupilAuthorization(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    status = db.Column(db.Boolean, nullable=True)
    comment = db.Column(db.String(50), nullable=True)
    created_by = db.Column(db.String(5), nullable= True)
    file_url = db.Column(db.String(50), nullable= True)

    #- RELATIONSHIP TO AUTHORIZATION MANY-TO-ONE
    origin_authorization = db.Column(db.String(50), db.ForeignKey('authorization.authorization_id'))
    authorized_pupil = db.relationship('Authorization', back_populates='authorized_pupils')

    #- RELATIONSHIP TO PUPIL MANY-TO-ONE
    pupil_id = db.Column(db.Integer, db.ForeignKey('pupil.internal_id'))
    pupil = db.relationship('Pupil', back_populates='authorizations')

    def __init__(self, pupil_id, origin_authorization, status, comment, created_by, file_url):
        self.pupil_id = pupil_id
        self.origin_authorization = origin_authorization
        self.status = status
        self.comment = comment
        self.created_by = created_by
        self.file_url = file_url
