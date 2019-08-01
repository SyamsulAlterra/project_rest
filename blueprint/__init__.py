from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from datetime import timedelta
from functools import wraps

import json

app = Flask(__name__)

app.config['APP_DEBUG'] = True

############################
# JWT 
############################
app.config['JWT_SECRET_KEY'] = 'thisissecret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

def internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['internal_status'] == 'internal':
            return {'status': 'FORBIDDEN', 'message': 'Internal Only'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

##########################
# DATABASE
##########################

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:alta321@localhost:3306/project_rest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


###################
# LOGGING
###################
@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except:
        requestData = request.args.to_dict()

    if response.status_code == 200:
        app.logger.warning('REQUEST_LOG\t%s', 
            json.dumps({
                'method': request.method,
                'code': response.status,
                'uri': request.full_path,
                'request': requestData,
                'response': json.loads(response.data.decode('utf-8'))
            })
        )

    return response

###############
# RESOURCES
###############

from .auth import bp_auth
from blueprint.user.resource import bp_user
from blueprint.event.resource import bp_event

app.register_blueprint(bp_auth, url_prefix='/login')
app.register_blueprint(bp_user, url_prefix='/user')


db.create_all()