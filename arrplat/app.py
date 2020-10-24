import os

from flask import Flask
from flask_cors import CORS

from extensions import db, jwt, swagger
from .setup import write_pid
from .resources.core.urls import blueprint as core_blueprint
from .resources.user.urls import blueprint as user_blueprint
from .resources.auth.urls import blueprint as auth_blueprint
from .resources.data_source.urls import blueprint as data_source_blueprint
from .resources.application.urls import blueprint as app_blueprint
from .resources.page.urls import blueprint as page_blueprint
from .resources.organization.urls import blueprint as org_blueprint
from arrplat.config import config
from .common.utils import DecimalEncoder

flask_env = os.environ.get("FLASK_ENV", "development")


def create_app():
    flask_app = Flask(__name__)
    flask_app.config = dict(flask_app.config, **config.get('system'))
    CORS(flask_app, supports_credentials=True)
#     setup_plugins.install_blueprint(flask_app)
    configure_extensions(flask_app)
    register_blueprints(flask_app)

    flask_app.json_encoder = DecimalEncoder
    write_pid.run()
    return flask_app


def configure_extensions(flask_app):
    db.init_app(flask_app)
    jwt.init_app(flask_app)
    if flask_env == "development":
        swagger.init_app(flask_app)


def register_blueprints(flask_app):
    flask_app.register_blueprint(user_blueprint, url_prefix='/user')
    flask_app.register_blueprint(auth_blueprint, url_prefix='/auth')
    flask_app.register_blueprint(core_blueprint, url_prefix='/core')
    flask_app.register_blueprint(app_blueprint, url_prefix='/app')
    flask_app.register_blueprint(page_blueprint, url_prefix='/page')
    flask_app.register_blueprint(org_blueprint, url_prefix='/org')
    flask_app.register_blueprint(data_source_blueprint, url_prefix='/data-source')


config_name = os.environ.get('API_CONFIG', 'development')
app = create_app()
