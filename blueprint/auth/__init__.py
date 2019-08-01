from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal

from flask_jwt_extended import create_access_token, get_jwt_claims, jwt_required
from blueprint import db

from ..user.model import User

bp_auth = Blueprint('auth',__name__)
api = Api(bp_auth)

class CreateTokenResource(Resource):
    def __init__(self):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='args', type=int, nullable=False)
        args = parser.parse_args()
        
        
        qry = User.query.get(args['id'])

        if qry is not None:
            qry_dict = marshal(qry, User.response_fields)
            token = create_access_token(identity = qry_dict['nama'], 
                                        user_claims={
                                            'id': qry_dict['id'],
                                            'status': qry_dict['status'],
                                            }
            )
            return {'token': token}, 200, {'Content-Type': 'application/json'}
        else:
            return {'message': 'there is no such query'}, 404, {'Content-Type': 'application/json'}


    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        return claims, 200, {'Content-Type': 'application/json'}


api.add_resource(CreateTokenResource, '/login')