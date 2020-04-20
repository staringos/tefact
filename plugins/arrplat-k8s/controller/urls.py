from flask import Blueprint
from flask_restful import Api

from .views import *

blueprint = Blueprint('/cluster', __name__, static_folder='static')
api = Api(blueprint)

api.add_resource(ClusterResource, '/<string:cluster_id>')
api.add_resource(ClusterListResource, '')

api.add_resource(ClusterDeploymentListResource, '/<string:cluster_id>/deployment')

api.add_resource(ClusterServiceListResource, '/<string:cluster_id>/service')

api.add_resource(ClusterIngressListResource, '/<string:cluster_id>/ingress')

api.add_resource(ClusterWebServerListResource, '/<string:cluster_id>/web/server')

