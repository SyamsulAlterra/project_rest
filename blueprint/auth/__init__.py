from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal

from flask_jwt_extended import create_access_token, get_jwt_claims, jwt_required
from blueprint import db

bp_auth = Blueprint('auth',__name__)
api = Api(bp_auth)

class CreateTokenResource(Resource):
    def __init__(self):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='args', type=int, nullable=False)
        args = parser.parse_args()
        
        
        qry = Client.query.get(args['id'])

        if qry is not None:
            qry_dict = marshal(qry, Client.response_fields)
            token = create_access_token(identity = qry_dict['name'], 
                                        user_claims={
                                            'id': qry_dict['id'],
                                            'nama': qry_dict['name'], 
                                            'internal_status': qry_dict['internal_status'],
                                            'id_penerbit': qry_dict['id_penerbit'],
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