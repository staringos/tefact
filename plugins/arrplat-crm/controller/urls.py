from flask import Blueprint
from flask_restful import Api

from .views import CustomerResource

blueprint = Blueprint('/crm', __name__, static_folder='static')
api = Api(blueprint)

api.add_resource(CustomerResource, '')
