from flask import Blueprint
from flask_restful import Api

from .views import PlatformConfig

blueprint = Blueprint('/platform', __name__, static_folder='static')
api = Api(blueprint)

api.add_resource(PlatformConfig, '/config')
