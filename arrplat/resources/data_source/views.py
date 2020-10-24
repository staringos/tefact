from flask_restful import Resource
from flask_apispec import use_kwargs
from marshmallow import fields
from .models import DataSource
from .schema import DataSourceSchema
from extensions import db
from arrplat.common.utils import json_response


class OrgDataSourceList(Resource):
    data_source_list_schema = DataSourceSchema(many=True)

    @use_kwargs({
        'plugins': fields.String(),
        'filename': fields.String()
    })
    def get(self, org_id):
        """数据源
          ---
          parameters:
            - name: org_id
              in: url
              type: string
              required: true
              description: 组织ID
          responses:
            200:
              examples:
                response: {"data": null, "message": "查询成功"}
        """

        data_list = db.session.query(DataSource).filter(DataSource.org_id == org_id).all()
        data = self.data_source_list_schema.dump(data_list).data

        return json_response(data=data, message="ok")


class DataSourceResource(Resource):

    def post(self, org_id):
        pass

    @use_kwargs({
        'plugins': fields.String(),
        'filename': fields.String()
    })
    def get(self, org_id):
        """数据源
          ---
          parameters:
            - name: org_id
              in: url
              type: string
              required: true
              description: 组织ID
          responses:
            200:
              examples:
                response: {"data": null, "message": "查询成功"}
        """
        pass
