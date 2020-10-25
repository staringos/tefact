from flask import Blueprint
from flask_restful import Api
from .views import DataSourceResource, OrgDataSourceList, DataSourceModifyResource, DataSourceTestResource, DataTableResource

blueprint = Blueprint('/data-source', __name__)
api = Api(blueprint)

api.add_resource(DataSourceTestResource, '/test/')
api.add_resource(OrgDataSourceList, '/org/<string:org_id>')
api.add_resource(DataSourceResource, '/')
api.add_resource(DataSourceModifyResource, '/<string:data_source_id>')
api.add_resource(DataTableResource, '/<string:data_source_id>/connect/table')
