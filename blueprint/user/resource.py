from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from .model import User
from blueprint.event.model import Event
from blueprint.eventguest.model import EventGuest
from blueprint import db, app,internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims
import requests, json, datetime

bp_user = Blueprint('user',__name__)
api = Api(bp_user)


class InvitationResource(Resource):
    def __init__(self):
        pass

    @jwt_required
    def get(self, id):
        claim=get_jwt_claims()
        qry=Event.query.get(id)
        if qry is None:
            return {'status':'EVENT_NOT_FOUND'},404

        location_host = 'https://api.ipgeolocation.io/ipgeo'
        location_apikey = 'fb1a8036e91f496092fb3a34f3abbb0f'
        currency_host = 'http://data.fixer.io/api/latest'
        currency_apikey = '1562319ae83fefd9bd13debd3b4a337b'
        solat_host='https://time.siswadi.com/pray/'
       

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
        currency_code_or = data['currency']['code']
        rates_or = currency_data['rates'][currency_code_or]

   
        hasil = marshal(qry,Event.response_fields)

        result={}

        rq = requests.get(location_host,params={'apiKey':location_apikey,'ip':hasil['ip']})
        event_location = rq.json()

        event_loc = event_location['district']+', '+event_location['city']+', '+event_location['state_prov']+', '+event_location['country_name']
        
        # sholat
        lat=event_location['latitude']
        lon=event_location['longitude']
        rq = requests.get(solat_host,params={'lat':lat,'lng':lon})
        solat = rq.json()
        jadwal_solat={
            'Fajr':solat['data']['Fajr'],
            'Dhuhr':solat['data']['Dhuhr'],
            'Asr':solat['data']['Asr'],
            'Maghrib':solat['data']['Maghrib'],
            'Isha':solat['data']['Isha'],
        }
        
        # negara
        currency_code_des=event_location['currency']['code']
        rates_des = currency_data['rates'][currency_code_des]
        exchange_rate=rates_or/rates_des
        # bahasa
        bahasa=event_location['languages']

        result['event_name']=hasil['nama']
        result['event_location'] = event_loc
        result['event_date'] = hasil['waktu']
        result['PIC'] = marshal(User.query.get(hasil['user_id']), User.response_fields)['nama']
        result['exchange_rate']='1 ' + currency_code_or +': '+str(exchange_rate)+' '+currency_code_des
        result['islamic_praying_time']=jadwal_solat
        result['language_to_learn']=bahasa

        evenguest_qry = EventGuest.query.filter_by(user_id=claim['id']).filter_by(event_id=id).first()
        if evenguest_qry is None:
            new_eventguest = EventGuest(claim['id'],id)

            db.session.add(new_eventguest)
            db.session.commit()

        qry=EventGuest.query.filter_by(event_id=id)
        guest_list=[]
        for gues in qry.all():
            # guest_name = marshal(gues,EventGuest.response_fields)
            guest_id = marshal(gues,EventGuest.response_fields)['user_id']
            guest_name=marshal(User.query.get(guest_id), User.response_fields)['nama']
            guest_list.append(guest_name)
      
        result['event_name']=hasil['nama']
        result['event_location'] = event_loc
        result['event_date'] = hasil['waktu']
        result['PIC'] = marshal(User.query.get(id), User.response_fields)['nama']
        result['exchange_rate']='1 ' + currency_code_or +': '+str(exchange_rate)+' '+currency_code_des
        result['islamic_praying_time']=jadwal_solat
        result['language_to_learn']=bahasa
        result['event_guest']=guest_list


        return result, 200, {'Content-Type':'application/json'}
      


class InternalUserResource(Resource):
    def __init__(self):
        pass

    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()

        parser.add_argument('p',type=int, location='args',default=1)
        parser.add_argument('rp',type=int, location='args',default=25)
        parser.add_argument('nama',location='args', help='invalid title value')
        # parser.add_argument('lokasi',location='args', help='invalid title value')        
        parser.add_argument('order_by_time',location='args', help='invalid sort value',choices=('desc','asc'))
        args = parser.parse_args()

        offset = (args['p']*args['rp'])-args['rp']

        qry=Event.query

        if args['nama'] is not None:
            qry=qry.filter_by(nama=args['nama'])

        if args['order_by_time'] is not None:
            if args['order_by_time'] == 'desc':
                qry = qry.order_by(Event.waktu.desc())
            else:
                qry = qry.order_by(Event.waktu)

        rows=[]
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row,Event.response_fields))

        return rows, 200, {'Content-Type':'application/json'}

    @jwt_required
    @internal_required
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('nama', location='json', required=True)
        parser.add_argument('ip', location='json', required=True)
        parser.add_argument('waktu', location='json', required=True)
        args = parser.parse_args()

        claim = get_jwt_claims()
        creator_id = claim['id']
        
        new_event = Event(args['nama'], args['ip'], args['waktu'], creator_id)

        app.logger.debug('DEBUG : %s', new_event)

        db.session.add(new_event)
        db.session.commit()

        return {'message': 'new event succesfully added'}, 200

    @jwt_required
    @internal_required
    def put(self, id):
        parser=reqparse.RequestParser()

        parser.add_argument('nama', location='json', required=True)
        parser.add_argument('ip', location='json', required=True)
        parser.add_argument('waktu', location='json', required=True)

        args = parser.parse_args()

        qry = Event.query.get(id)
        if qry is None:
            return {'status' : 'NOT_FOUND', 'message':'User not found'}, 404

        qry = marshal(qry, Event.response_fields)

        if qry['user_id'] == get_jwt_claims()['id']:
            external_user_id=get_jwt_claims()['id']

            qry.nama = args['nama']
            qry.ip = args['ip']
            qry.waktu = args['waktu']
            qry.user_id = external_user_id
            db.session.commit()

            return marshal(qry,Event.response_fields), 200, {'Content-Type':'application/json'}

        return {'message': 'you can only edit your own event'}, 403

            
    @jwt_required
    @internal_required
    def delete(self, id):
        qry = Event.query.get(id)
        if qry == None:
            return {'message': 'event not found'}, 404

        qry2 = marshal(qry, Event.response_fields)
        if qry2['user_id'] == get_jwt_claims()['id']:
            eventguest_qry = EventGuest.query.filter_by(event_id=id).all()
            for eventguest in eventguest_qry:
                db.session.delete(eventguest)
                db.session.commit()
                
            db.session.delete(qry)
            db.session.commit()

            return {'message': 'event succesfully deleted'}, 200

        return {'message': 'you can only delete your own event'}, 403
   

api.add_resource(InvitationResource,'/get_event/<id>')
api.add_resource(InternalUserResource, '/event', '/event/<id>')

