from flask import Blueprint
from flask_restful import Api
from .views import SharePageResource, AddShareResource, SharePageDetailsResource

blueprint = Blueprint('/s', __name__)
api = Api(blueprint)

api.add_resource(SharePageResource, '/p/<string:key>')
api.add_resource(SharePageDetailsResource, '/p/<string:key>/d')
api.add_resource(AddShareResource, '/p/<string:page_id>')
