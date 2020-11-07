from flask import Blueprint
from flask_restful import Api
from .views import SharePageResource, AddShareResource

blueprint = Blueprint('/s', __name__)
api = Api(blueprint)

api.add_resource(SharePageResource, '/<string:share_key>')
api.add_resource(AddShareResource, '/p/<string:page_id>')
