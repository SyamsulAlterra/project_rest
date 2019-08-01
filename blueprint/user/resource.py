from flask import Flask, request, Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from .model import User
from ..event.model import Events
from blueprint import app, db, internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims
import requests, json

bp_user = Blueprint('user', __name__)
api = Api(bp_user)

class UserResource(Resource):
    def __init__(self):
        pass

    @jwt_required
    def get(self):
        claim = get_jwt_claims()
        all_event = Events.query.all()

        if all_event == None:
            return {'message': 'no event'}, 404

        event_list=[]
        for event in all_event:
            event_dict = marshal(event, Events.response_fields)
            event_list.append(event_dict)

        return event_list, 200

    @jwt_required
    @internal_required
    def post(self):
        claim = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('nama', location=args, required=True)
        parser.add_argument('ip', locations=args, required=True)
        parser.add_argument('waktu', locations=args, required=True)
        args = parser.parse_args()
        creator_id = claim['id']
        
        new_event = Events(args['nama'], args['ip'], args['waktu'], creator_id)

        db.session.add(new_event)
        db.session.commit()

        return {'message': 'new event succesfully added'}, 200

    @jwt_required
    @internal_required
    def delete(self, id):
        qry = Events.get(id)
        if qry == None:
            return {'message': 'event not found'}, 404

        db.session.delete(qry)
        db.session.commit()

        return {'message': 'event succesfully deleted'}, 200

class InvitationResource(Resource):
    def __init__(self):
        pass

    @jwt_required
    def get(self, id):
        location_host = 'https://api.ipgeolocation.io/ipgeo'
        location_apikey = 'fb1a8036e91f496092fb3a34f3abbb0f'
        currency_host = 'http://data.fixer.io/api/latest'
        currency_apikey = '1562319ae83fefd9bd13debd3b4a337b'
        tes = id

        my_ip = requests.get('https://ip.seeip.org/json')
        my_ip = my_ip.json()['ip']

        data = requests.get(location_host, params={
            'apiKey': location_apikey,
            'ip': my_ip
        })
        data = data.json()

        currency_data = requests.get(currency_host, params={'access_key': currency_apikey})
        currency_data = currency_data.json()


        my_location = data['district']+', '+data['city']+', '+data['state_prov']+', '+data['country_name']
        currency_code = data['currency']['code']
        rates = currency_data['rates'][currency_code]

        result ={
            'my_location': my_location,
            'currency_code': currency_code,
            'rates': rates
        }

        return result, 200
        

api.add_resource(UserResource, '', '/<id>')
api.add_resource(InvitationResource, '/event/<id>')

#     @jwt_required
#     def get(self, id):
#         claims = get_jwt_claims()
#         qry = User.query.get(id)
#         if qry == None:
#             return {'message': 'user not found'}, 404, {'Content-Type': 'application/json'}

#         if claims['client_status'] == 1:
#             return marshal(qry, User.response_fields), 200, {'Content-Type': 'application/json'}
#         else:
#             if claims['client_id'] == qry.client_id:
#                 return marshal(qry, User.response_fields), 200, {'Content-Type': 'application/json'}
#             else:
#                 return {'message': 'You don\'t have permission to access this'}, 403, {'Content-Type': 'application/json'}

    
#     @jwt_required
#     @internal_required
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('name', location='json')
#         parser.add_argument('age', location='json', type=int)
#         parser.add_argument('sex', location='json')
#         parser.add_argument('client_id', location='json', type=int)
#         args = parser.parse_args()

#         user = User(args['name'], args['age'], args['sex'], args['client_id'])

#         db.session.add(user)
#         db.session.commit()

#         app.logger.debug('DEBUG : %S', user)

#         return marshal(user, User.response_fields), 200, {'Content-Type': 'application/json'}

#     @jwt_required
#     @internal_required
#     def put(self, id):
#         parser = reqparse.RequestParser()
#         parser.add_argument('name', location='json')
#         parser.add_argument('age', location='json')
#         parser.add_argument('sex', location='json')
#         parser.add_argument('client_id', location='json', type=int)
#         args = parser.parse_args()

#         qry = User.query.get(id)
#         if qry == None:
#             return {'message': 'user not found'}, 404, {'Content-Type': 'application/json'}
        
#         qry.name = args['name']
#         qry.age = args['age']
#         qry.sex = args['sex']
#         qry.client_id = args['client_id']
#         db.session.commit()

#         return marshal(qry, User.response_fields), 200, {'Content-Type': 'application/json'}

#     @jwt_required
#     @internal_required
#     def delete(self, id):
#         qry = User.query.get(id)
#         if qry == None:
#             return {'message': 'user not found'}, 404, {'Content-Type': 'application/json'}

#         db.session.delete(qry)
#         db.session.commit()

#         return {'message': 'delete succes'}, 200, {'Content-Type': 'application/json'}

# class UserList(Resource):
#     def __init__(self):
#         pass

#     @jwt_required
#     def get(self):
#         claims = get_jwt_claims()
#         parser = reqparse.RequestParser()
#         parser.add_argument('p', location='args', type=int, default=1)
#         parser.add_argument('rp', location='args', type=int, default=25)
#         parser.add_argument('age', location='args')
#         args = parser.parse_args()

#         offset = args['p']*args['rp']-args['rp']

#         qry = User.query
#         if qry == None:
#             return {'message': 'user not found'}, 404, {'Content-Type': 'application/json'}
        
#         if args['age'] is not None:
#             qry = qry.filter_by(age=args['age'])
        
#         clients = []
#         for client in qry.limit(args['rp']).offset(offset).all():
#             if claims['client_status'] == 1:
#                 clients.append(marshal(client, User.response_fields))
#             else:
#                 if claims['client_id'] == client.client_id:
#                     clients.append(marshal(client, User.response_fields))

#         return clients, 200, {'Content-Type': 'application/json'}


# api.add_resource(UserResource, '', '/<id>')
# api.add_resource(UserList, '/list')