from marshmallow import Schema, fields

from arrplat.resources.user.models import User, UserInfo


class UserInfoSchema(Schema):
    id = fields.String()
    gender = fields.Integer()
    head_url = fields.String()
    signature = fields.String()
    email = fields.String()

    class Meta:
        model = UserInfo


class UserSchema(Schema):
    id = fields.String()
    head_url = fields.String()
    name = fields.String()
    nickname = fields.String()
    phone = fields.String()
    user_info = fields.Nested(UserInfoSchema)

    class Meta:
        model = User
