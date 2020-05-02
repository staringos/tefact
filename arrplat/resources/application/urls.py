from flask import Blueprint
from flask_restful import Api
from .views import LightAppResource, LightAppModifyResource, LightAppMenu, LightAppPage, LightPageResource, PageSectionResource, PageSectionListResource

blueprint = Blueprint('app', __name__)
api = Api(blueprint)

api.add_resource(LightAppResource, '/light')
api.add_resource(LightAppModifyResource, '/light/<string:id>')

api.add_resource(LightAppMenu, '/light/menu')
api.add_resource(LightAppPage, '/light/page')

api.add_resource(LightPageResource, '/light/page/<string:id>')
api.add_resource(PageSectionListResource, '/light/page/<string:page_id>/section')
api.add_resource(PageSectionResource, '/light/page/<string:page_id>/section/<string:section_id>')

