from flask_restful import fields
from blueprint import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(100))
    status = db.Column(db.String(10), default='non-internal', nullable=False)

    response_fields={
        'id': fields.Integer,
        'nama': fields.String,
        'status': fields.String,
    }

    def __init__(self, nama, status):
        self.nama = nama
        self.status = status

    def __repr__(self):
        return str(self.id) + self.nama
