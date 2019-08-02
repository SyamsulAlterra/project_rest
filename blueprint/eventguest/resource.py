from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from .model import EventGuest
from blueprint import db, app,internal_required
from flask_jwt_extended import jwt_required

bp_eventguest = Blueprint('eventguest',__name__)
api = Api(bp_eventguest)