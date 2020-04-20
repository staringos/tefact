from flask import Blueprint
from flask_restful import Api
from .views import PhoneCodeResource, VerifyCodeResource, PasswordLoginResource, PhoneLoginResource, \
    PasswordRegisterResource, PasswordVerifyResource

blueprint = Blueprint('auth', __name__)
api = Api(blueprint)

api.add_resource(PhoneCodeResource, '/phone/code')
api.add_resource(PhoneLoginResource, '/phone/login')

api.add_resource(VerifyCodeResource, '/verify-code')
api.add_resource(PasswordLoginResource, '/login')
api.add_resource(PasswordRegisterResource, '/register')
api.add_resource(PasswordVerifyResource, '/password/modify')


