from blueprint import db
from flask_restful import fields

class Events(db.Model):
    __tablename__='event'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama=db.Column(db.String(30), nullable=False)
    ip=db.Column(db.String(20), nullable=False)
    waktu=db.Column(db.DateTime, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    response_fields={
        'id': fields.Integer,
        'nama': fields.String,
        'ip': fields.String,
        'waktu': fields.String,
        'user_id': fields.Integer
    }

    def __init__(self,nama,ip,waktu,user_id):
        self.nama=nama
        self.ip=ip
        self.waktu=waktu
        self.user_id=user_id

    def __repr__(self):
        return '<Event %r>' %self.id