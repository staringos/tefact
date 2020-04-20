from flask import Blueprint
from flask_restful import Api
from .views import LightAppResource, LightAppModifyResource, LightAppMenu, LightAppPage

blueprint = Blueprint('app', __name__)
api = Api(blueprint)

api.add_resource(LightAppResource, '/light')
api.add_resource(LightAppModifyResource, '/light/<string:id>')

api.add_resource(LightAppMenu, '/light/menu')
api.add_resource(LightAppPage, '/light/page')
