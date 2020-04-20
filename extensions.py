from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flasgger import Swagger
from passlib.context import CryptContext

db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
pwd_context = CryptContext(schemes=['pbkdf2_sha256'], deprecated='auto')
swagger = Swagger()
