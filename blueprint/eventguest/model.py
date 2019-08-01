from flask_restful import fields
from blueprint import db

class EventGuest(db.Model):
    __tablename__ = 'eventguest'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

    response_fields={
        'id': fields.Integer,
        'user_id': fields.Integer,
        'event_id': fields.Integer,
    }

    def __init__(self, user_id, event_id):
        self.user_id = user_id
        self.event_id = event_id

    def __repr__(self):
        return str(self.id) + str(self.user_id) + str(self.event_id)
