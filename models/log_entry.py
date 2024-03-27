from .schoolday import *

class LogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    user = db.Column(db.String(5))
    endpoint = db.Column(db.String(100))
    payload = db.Column(db.String(500))
    def __init__(self, datetime, user, endpoint, payload):
        self.datetime = datetime
        self.user = user
        self.endpoint = endpoint
        self.payload = payload
