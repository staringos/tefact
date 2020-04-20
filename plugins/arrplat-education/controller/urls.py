from flask import Blueprint
from flask_restful import Api

from .views import  CourseResource, EmployeeResource, BaseCourseResource, InstrumentTypeResource, \
    CampusClassroomResource, StudentResource, CourseLevelResource, MaterialResource, CustomerResource, \
    CourseSignResource, StudentLevelResource, StudentDetailResource, StudentCourseResource, OrderResource,\
    CourseTypeResource, UserHistoryResource, StudentRemarkResource, InstrumentUseResource

blueprint = Blueprint('/edu', __name__, static_folder='static')
api = Api(blueprint)

api.add_resource(CourseResource, '/course')

api.add_resource(EmployeeResource, "/employee")
api.add_resource(InstrumentTypeResource, "/instrumentType")
api.add_resource(BaseCourseResource, "/baseCourse")
api.add_resource(CampusClassroomResource, "/campusClassroom")
api.add_resource(StudentResource, "/student")
api.add_resource(StudentCourseResource, "/studentCourse")
api.add_resource(StudentDetailResource, "/studentDetail")
api.add_resource(CourseLevelResource, "/courseLevel")
api.add_resource(MaterialResource, "/material")
api.add_resource(CustomerResource, "/customer")
api.add_resource(CourseSignResource, "/courseSign")
api.add_resource(StudentLevelResource, "/studentLevel")
api.add_resource(OrderResource, "/order")
api.add_resource(CourseTypeResource, "/courseType")
api.add_resource(UserHistoryResource, "/userHistory")
api.add_resource(StudentRemarkResource, "/studentRemark")
api.add_resource(InstrumentUseResource, "/instrumentUse")
