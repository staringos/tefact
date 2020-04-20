from marshmallow import Schema, fields

from .models import Cluster


class ClusterSchema(Schema):
    id = fields.String()
    name = fields.String()
    host = fields.String()
    port = fields.Integer()
    token = fields.String()
    create_time = fields.Integer()
    user_id = fields.String()

    class Meta:
        model = Cluster
