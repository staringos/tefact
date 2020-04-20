from flask import Blueprint
from flask_restful import Api
from .upload import FileUpload
from .views import PluginsStatic

blueprint = Blueprint('core', __name__)
api = Api(blueprint)

api.add_resource(FileUpload, '/upload-files/<string:bucket_name>')
api.add_resource(PluginsStatic, '/plugins/<string:plugins>/static/<string:filename>', endpoint='hahaha')
