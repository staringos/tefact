from flask import Blueprint
from flask_restful import Api

from .views import *

blueprint = Blueprint('/org', __name__, static_folder='static')
api = Api(blueprint)

api.add_resource(CreateOrganizationResource, '')
api.add_resource(OrganizationResource, '/<string:org_id>')
api.add_resource(OrganizationListResource, '/list')

api.add_resource(CreateOrgDepartmentResource, '/<string:org_id>/department')
api.add_resource(OrgDepartmentResource, '/<string:org_id>/department/<string:org_department_id>')
api.add_resource(OrgDepartmentListResource, '/<string:org_id>/department/list')
api.add_resource(OrgDepartmentStaffListResource, '/<string:org_id>/department/<string:org_department_id>/staff')

api.add_resource(OrgApplicationDetailResource, '/<string:org_id>/app/<string:app_id>')
api.add_resource(OrgApplicationResource, '/<string:org_id>/app')

api.add_resource(OrgStaffResource, '/<string:org_id>/staff/<string:staff_id>')
api.add_resource(OrgCreateStaffResource, '/<string:org_id>/staff')

api.add_resource(OrgAuthMenuResource, '/<string:org_id>/auth')

api.add_resource(OrgRoleResource, '/<string:org_id>/role')
api.add_resource(OrgRoleDetailResource, '/<string:org_id>/role/<string:role_id>')
api.add_resource(OrgAuthRoleStaffResource, '/<string:org_id>/role/<string:role_id>/staff')
api.add_resource(OrgAuthRoleResource, '/<string:org_id>/role/<string:role_id>/auth')
