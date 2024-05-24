from .schoolday import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    role = db.Column(db.String(10), nullable = True)
    tutoring = db.Column(db.String(10), nullable = True)
    credit = db.Column(db.Integer, nullable = True)
    time_units = db.Column(db.Integer, nullable = True)
    contact = db.Column(db.String(50), nullable = True)

    def __init__(self, public_id, name, password, admin, role, tutoring, credit, time_units, contact):
        self.public_id = public_id
        self.name = name
        self.password = password
        self.admin = admin
        self.role = role
        self.tutoring = tutoring
        self.credit = credit
        self.time_units = time_units
        self.contact = contact




