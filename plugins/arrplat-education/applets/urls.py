"""
@author xiaofei
@date   2020-02-28
@desc
"""
from flask import Blueprint
from flask_restful import Api
from .views import BannerResource, ArticleResource, CourseResource, CourseSignResource, BaseInfoResource, \
    StudentResource, CustomerResource, EmployeeResource,LoginResource, LearnResource

blueprint = Blueprint('/edu/applets', __name__, static_folder='static')
api = Api(blueprint)
api.add_resource(BannerResource, '/banner')
api.add_resource(ArticleResource, '/article')
api.add_resource(CourseResource, "/course")
api.add_resource(CourseSignResource, "/courseSign")
api.add_resource(BaseInfoResource, "/baseInfo")
api.add_resource(StudentResource, "/student")
api.add_resource(CustomerResource, "/customer")
api.add_resource(EmployeeResource, "/employee")
api.add_resource(LoginResource, "/login")
api.add_resource(LearnResource, "/learn")
