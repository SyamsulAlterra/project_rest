from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from .model import Event
from blueprint import db, app,internal_required
from flask_jwt_extended import jwt_required

bp_event = Blueprint('event',__name__)
api = Api(bp_event)