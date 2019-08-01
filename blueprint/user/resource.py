from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from .model import User
from blueprint.event.model import Event
from blueprint import db, app,internal_required
from flask_jwt_extended import jwt_required
import requests

bp_user = Blueprint('user',__name__)
api = Api(bp_user)


class ExternalUserResource(Resource):
    lokasi_host='https://api.ipgeolocation.io/ipgeo'
    lokasi_key='fb1a8036e91f496092fb3a34f3abbb0f'

    solat_host='https://time.siswadi.com/pray/'

    def __init__(self):
        pass

    # @jwt_required
    # @internal_required
    def get(self,id):
        qry=Event.query.get(id)
        if qry is None:
            return {'status':'EVENT_NOT_FOUND'},404
        result = marshal(qry,Event.response_fields)

        rq = requests.get(self.lokasi_host,params={'apiKey':self.lokasi_key,'ip':result['ip']})
        lokasi = rq.json()

        # sholat
        lat=lokasi['latitude']
        lon=lokasi['longitude']
        rq = requests.get(self.solat_host,params={'lat':lat,'lng':lon})
        solat = rq.json()
        jadwal_solat={
            'Fajr':solat['data']['Fajr'],
            'Dhuhr':solat['data']['Dhuhr'],
            'Asr':solat['data']['Asr'],
            'Maghrib':solat['data']['Maghrib'],
            'Isha':solat['data']['Isha'],
        }
        # negara
        negara=lokasi['currency']['code']

        # bahasa
        bahasa=lokasi['languages']

        result['mata_uang']=negara
        result['jadwal_sholat']=jadwal_solat
        result['bahasa']=bahasa


        return result, 200, {'Content-Type':'application/json'}



def put(self, id):
        parser=reqparse.RequestParser()

        parser.add_argument('nama',location='json',required=True)
        parser.add_argument('waktu',location='json',required=True)

        args = parser.parse_args()
        
        qry = Event.query.get(id)

        if qry is None:
            return {'status' : 'NOT_FOUND', 'message':'User not found'}, 404
        
        rq=requests.get('https://ip.seeip.org/json')
        external_user_ip=rq.json()

        data = parser.parse_args()
        external_user_id=get_jwt_claims()['id']

        qry.nama = args['nama']
        qry.ip = external_user_ip
        qry.waktu = args['waktu']
        qry.user_id = external_user_id
        db.session.commit()

        return marshal(qry,Event.response_fields), 200, {'Content-Type':'application/json'}



class ExternalUserList(Resource):
    def __init__(self):
        pass
    
    # @jwt_required
    # @internal_required
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

api.add_resource(ExternalUserList,'','/list')
api.add_resource(ExternalUserResource,'','/<id>')