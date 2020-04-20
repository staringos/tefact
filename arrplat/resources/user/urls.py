from flask import Blueprint
from flask_restful import Api
from .views import UserInfoResource, UserInviteesMessage, UserMessageResource, UserMessageDetailResource,\
    UserOrganizationResource

blueprint = Blueprint('user', __name__)
api = Api(blueprint)

api.add_resource(UserInfoResource, '/info')

api.add_resource(UserInviteesMessage, '/org/request/<string:org_request_id>')
api.add_resource(UserMessageDetailResource, '/message/<string:message_id>')
api.add_resource(UserMessageResource, '/message')
api.add_resource(UserOrganizationResource, '/org/<string:org_id>')
