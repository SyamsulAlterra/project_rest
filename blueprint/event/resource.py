from flask import Flask, request, Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from .model import Events
from blueprint import app, db, internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_event = Blueprint('event', __name__)
api = Api(bp_event)