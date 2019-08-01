from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from .model import User
from blueprint import db, app,internal_required
from flask_jwt_extended import jwt_required

bp_user = Blueprint('user',__name__)
api = Api(bp_user)