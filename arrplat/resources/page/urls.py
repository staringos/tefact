from flask import Blueprint
from flask_restful import Api

from .views import PageResource, PageSectionResource, PageSectionEntityResource, \
    EntityOptionResource, EntityResource, EntityDataResource, DataSourceResource, DataSourceEntityResource

blueprint = Blueprint('page', __name__)
api = Api(blueprint)

api.add_resource(PageResource, '/<string:page_key>')
api.add_resource(PageSectionResource, '/section/<string:page_section_id>')
api.add_resource(PageSectionEntityResource, '/section/entity/<string:entity_id>')
api.add_resource(EntityResource, '/entity/<string:entity_key>')
api.add_resource(EntityDataResource, '/entity/data/<string:id>')
api.add_resource(EntityOptionResource, '/section/entity/<string:entity_id>/option')

api.add_resource(DataSourceResource, '/data-source')

api.add_resource(DataSourceEntityResource, '/data-source/<string:id>')
