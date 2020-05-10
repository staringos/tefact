from flask import request
from marshmallow import fields, Schema
from flask_apispec import use_kwargs
from flask_restful import Resource
from sqlalchemy import and_
import pendulum

from arrplat.common.auth_jwt_utils import user_required
from extensions import db
from arrplat.config import DEFAULT_PAGE, DEFAULT_PAGE_SIZE
from arrplat.common.utils import json_response, valid_uuid, valid_not_blank, generate_uuid
from arrplat.resources.page.schema import PageSchema, PageSectionSchema, \
    EntityOptionSchema, EntityFieldsSchema, EntitySchema, DataSourceSchema, EntitySimpleSchema
from arrplat.resources.page.models import Page, PageSection, Entity, EntityField, DataSource


class QueryPageSchema(Schema):
    page = fields.Integer(True, default=DEFAULT_PAGE, validate=lambda page: page > 0)
    size = fields.Integer(required=False, default=DEFAULT_PAGE_SIZE, validate=lambda size: size > 0)


class QuerySearchFieldConditionSchema(Schema):
    field_name = fields.String(required=True)
    value = fields.String(required=True)


class QuerySortSchema(Schema):
    field_name = fields.String(required=False)
    order = fields.String(required=False, default='asc')


class DataSourceResource(Resource):
    @user_required
    @use_kwargs({
        "application_id": fields.String(required=True),
        "name": fields.String(required=True),
        "type": fields.String(required=True),
        "connect_url": fields.String(required=False),
        "file_url": fields.String(required=False),
        "username": fields.String(required=False),
        "password": fields.String(required=False),
    })
    def post(self, **kwargs):
        """添加数据源
          ---
          tags:
            - 数据源
          parameters:
            - name: application_id
              in: data
              type: string
              required: true
              description: 应用ID
            - name: name
              in: data
              type: string
              required: true
              description: 数据源名称
            - name: type
              in: data
              type: string
              required: true
              description: 数据源类型
            - name: application_id
              in: data
              type: string
              required: true
              description: 应用ID
            - name: connect_url
              in: data
              type: string
              required: true
              description: 数据源连接URL
            - name: username
              in: data
              type: string
              required: true
              description: 数据源用户名
            - name: password
              in: data
              type: string
              required: true
              description: 数据源密码
          - name: file_url
              in: data
              type: string
              required: true
              description: 数据源文件路径
          responses:
            status:
              description:
        """
        data_source = DataSource(
            application_id=kwargs.get("application_id"),
            name=kwargs.get("name"),
            type=DataSource.string_to_type(kwargs.get("type")),
            connect_url=kwargs.get("connect_url"),
            file_url=kwargs.get("file_url"),
            username=kwargs.get("username"),
            password=kwargs.get("password"),
        )
        db.session.add(data_source)
        db.session.commit()
        return json_response("添加成功")


class DataSourceEntityResource(Resource):
    data_source_schema = DataSourceSchema(many=False)
    entity_simple_schema = EntitySimpleSchema(many=True)

    @user_required
    def get(self, id):
        data_source = db.session.query(DataSource) \
            .join(Page, and_(DataSource.id == id)) \
            .first()

        if not data_source:
            return json_response(message="找不到对应的数据源", status=404)

        entities = db.session.query(Entity) \
            .join(Page, and_(Entity.data_source_id == id)).all()
        data = self.data_source_schema.dump(data_source).data
        data["entities"] = self.entity_simple_schema.dump(entities).data

        return json_response(data=data)


class PageResource(Resource):
    @user_required
    def get(self, page_key):
        """菜单页面
          ---
          tags:
            - page页面数据
          parameters:
            - name: page_key
              in: url
              type: string
              required: true
              description: Application Key 应用key
            - name: org_id
              in: querystring
              type: string
              required: false
              description: 组织id
          responses:
            status:
              description:
              examples:
                response: {"data": {
                  "page_section": [
                    {
                      "entity": {
                        "entity_data": [],
                        "entity_field": []
                      }
                    }
                  ]
                }}
        """
        page_object = Page.query.filter(Page.key == page_key) \
            .first()
        page_schema = PageSchema()
        # try:
        data = page_schema.dump(page_object).data
        # except Exception as e:
        #     return json_response(message=str(e), status=403)
        db.session.commit()
        return json_response(data=data)


class PageSectionResource(Resource):
    @user_required
    @use_kwargs({
        "page": fields.Nested(QueryPageSchema),
        # "search_condition": fields.List(fields.Nested(QuerySearchFieldConditionSchema)),
        "search_condition": fields.List(fields.Dict()),
        "sort": fields.Nested(QuerySortSchema),
        "params": fields.Dict()
    })
    def post(self, page_section_id, **kwargs):
        """页面某一块的数据
          路由中存在几个参数
            - app_id, page_section_id 在路由中
            - page, search_condition, sort

           如果 search_condition的的字段存在使用id去查询，那么表示是数据详情
          ---
          tags:
            - page页面数据
          parameters:
            - name: page_section_id
              in: path
              type: string
              required: true
              enum: ['12363708151a46879f3efb76780c5ba9']
              description: 页面块id
            - name: page
              in: body
              type: object
              required: false
              description: 分页
              example:
                value: [{"page": 1, "size": 10}]
            - name: search_condition
              in: body
              type: object
              required: false
              description: 搜索
              example:
                value: [{"field_name": "id", "value": "12363708151a46879f3efb76780c5ba9"}]
            - name: sort
              in: body
              type: object
              required: false
              description: 排序
              example:
                value: {"field_name": "id", "order": "asc"}
            - name: org_id
              in: body
              type: string
              required: false
              description: 组织id
            - name: params
              in: body
              type: object
              required: false
              description: 参数
          responses:
            status:
              description:
              examples:
                response: {}
        """
        if kwargs.get("page") and not kwargs["page"].get("size"):
            kwargs["page"]["size"] = DEFAULT_PAGE_SIZE
        page_section = db.session.query(PageSection) \
            .join(Page, and_(PageSection.page_id == Page.id, PageSection.id == page_section_id)) \
            .first()
        if not page_section:
            return json_response(message="找不到对应的page_section", status=404)

        try:
            if 'params' in kwargs:
                setattr(page_section, 'detail_params', kwargs.pop('params'))
            page_section_schema = PageSectionSchema(**kwargs)
            data = page_section_schema.dump(page_section).data
        except Exception as e:
            return json_response(message=str(e), status=403)
        db.session.commit()
        return json_response(data=data)


class PageSectionEntityResource(Resource):
    @user_required
    @use_kwargs({
        "data": fields.Dict(required=True, validate=valid_not_blank)
    })
    def post(self, entity_id: str, data: dict):
        """页面某一块section数据添加

          ---
          tags:
            - page页面数据
          parameters:
            - name: entity_id
              in: path
              type: string
              required: true
              enum: ['12363708151a46879f3efb76780c5ba9']
              description: 实例id
            - name: data
              in: body
              type: string
              required: true
              enum: [{"name": "123", 'age': 13}]
              description: 数据体
            - name: org_id
              in: body
              type: string
              required: false
              description: 组织id
          responses:
            200:
              description:  成功
              examples:
                response: {"message": "ok"}
        """
        try:
            table_name, _ = self.get_table_name(entity_id=entity_id)
        except Exception as e:
            _ = e
            return json_response(message=str(e), status=404)

        try:
            # 关联表会用到
            data_id = generate_uuid()
            data["id"] = data_id

            # 检验数据
            message, status = self.verify_field(entity_id, data, table_name)
            if status != 0:
                return json_response(message=message, status=status)

            # 查询是否有多对多关系 存储关联表
            entity_fields = EntityField.query.filter_by(entity_id=entity_id, foreign_type=2).all()
            insert_sql_foreign_all = []
            for field in entity_fields:
                # foreign_type = field.foreign_type
                field_key = field.key
                foreign_table_name = field.foreign_table_name
                foreign_our_key = field.foreign_our_key
                foreign_their_key = field.foreign_their_key

                if field_key in data.keys():
                    # 多个的值
                    key_values = data[field_key]
                    # 主表不用再插入
                    data.pop(field_key)
                    if not key_values:
                        continue
                else:
                    # 没数据
                    continue

                field_str_foreign = 'id,' + foreign_our_key + ',' + foreign_their_key
                value_str_foreign = ','.join("('%s','%s','%s')" % (generate_uuid(), data_id, v) for v in key_values)
                insert_sql_foreign = "INSERT INTO %s (%s) VALUES %s;" % (
                    foreign_table_name, field_str_foreign, value_str_foreign)
                insert_sql_foreign_all.append(insert_sql_foreign)
                # 不能先执行 会有外键问题
                # db.session.execute(insert_sql_foreign)

            # 查询是否有create_time或者别的字段
            entity_fields_all = EntityField.query.filter_by(entity_id=entity_id).all()
            int_timestamp = pendulum.now('Asia/Shanghai').int_timestamp
            for field in entity_fields_all:
                field_key = field.key
                if field_key == 'create_time':
                    data[field_key] = int_timestamp
                if field_key == 'update_time':
                    data[field_key] = int_timestamp

            # 主表数据
            field_dict = dict()
            for key, value in data.items():
                if isinstance(value, list) or isinstance(value, dict):
                    continue
                field_dict[key] = value
            field_str = ",".join(field_dict.keys())
            value_str = ",".join([":%s" % field for field in field_dict.keys()])
            insert_sql = "INSERT INTO %s(%s) VALUE(%s);" % (table_name, field_str, value_str)

            # 主表数据先插入 否则关联表外键有问题
            db.session.execute(insert_sql, data)
            # 再插入关联表
            for sql in insert_sql_foreign_all:
                db.session.execute(sql)
            # db.session.commit()
        except Exception as e:
            _ = e
            print(e)
            db.session.rollback()
            return json_response(message="数据添加失败，%s" % str(e), status=500)
        else:
            db.session.commit()
            return json_response(message='ok')

    @user_required
    @use_kwargs({
        "data_id": fields.String(required=True, validate=valid_uuid),
        "data": fields.Dict(required=True, validate=valid_not_blank)
    })
    def put(self, entity_id: str, data_id: str, data: dict):
        """页面某一块section数据-修改

          ---
          tags:
            - page页面数据
          parameters:
            - name: entity_id
              in: path
              type: string
              required: true
              enum: ['12363708151a46879f3efb76780c5ba9']
              description: 实例id
            - name: data_id
              in: path
              type: string
              required: true
              enum: ['12363708151a46879f3efb76780c5ba9']
              description: 要修改的数据id
            - name: data
              in: body
              type: object
              required: true
              example: {"name": "xxx", "description": "xxxx"}
              description: 数据
            - name: org_id
              in: querystring
              type: string
              required: false
              description: 组织id
          responses:
            200:
              description:  成功
              examples:
                response: {"message": "ok"}
        """
        try:
            table_name, condition = self.get_table_name(entity_id=entity_id, data_id=data_id)
        except Exception as e:
            _ = e
            return json_response(message=str(e), status=404)

        # 检验数据
        message, status = self.verify_field(entity_id, data, table_name, data_id)
        if status != 0:
            return json_response(message=message, status=status)

        # TODO 该部分与psot接口重复度高 可复用
        # 查询是否有多对多关系 更新关联表 先删后加
        entity_fields = EntityField.query.filter_by(entity_id=entity_id, foreign_type=2).all()
        insert_sql_foreign_all = []
        delete_sql_foreign_all = []
        for field in entity_fields:
            # foreign_type = field.foreign_type
            field_key = field.key
            foreign_table_name = field.foreign_table_name
            foreign_our_key = field.foreign_our_key
            foreign_their_key = field.foreign_their_key

            # 关联表先删除数据
            delete_sql = "DELETE FROM %s WHERE %s='%s'" % (foreign_table_name, foreign_our_key, data_id)
            delete_sql_foreign_all.append(delete_sql)
            if field_key in data.keys():
                # 多个的值
                key_values = data[field_key]
                # 主表不用再插入
                data.pop(field_key)
                if not key_values:
                    continue
            else:
                # 没数据
                continue

            field_str_foreign = 'id,' + foreign_our_key + ',' + foreign_their_key
            value_str_foreign = ','.join("('%s','%s','%s')" % (generate_uuid(), data_id, v) for v in key_values)
            insert_sql_foreign = "INSERT INTO %s (%s) VALUES %s;" % (
                foreign_table_name, field_str_foreign, value_str_foreign)
            insert_sql_foreign_all.append(insert_sql_foreign)

        # 查询是否有update_time
        entity_fields_all = EntityField.query.filter_by(entity_id=entity_id).all()
        int_timestamp = pendulum.now('Asia/Shanghai').int_timestamp
        for field in entity_fields_all:
            field_key = field.key
            # if field_key == 'create_time':
            #     data[field_key] = int_timestamp
            if field_key == 'update_time':
                data[field_key] = int_timestamp
        field_list = list()
        for key, value in data.items():
            if isinstance(value, list) or isinstance(value, dict):
                continue
            field_list.append('%s=:%s' % (key, key))
        field_str = ','.join(field_list)
        update_sql = "UPDATE %s SET %s WHERE %s;" % (table_name, field_str, condition)

        try:
            # 更新主表
            db.session.execute(update_sql, data)
            # 关联表先删除数据
            for sql in delete_sql_foreign_all:
                db.session.execute(sql)
            # 再插入关联表
            for sql in insert_sql_foreign_all:
                db.session.execute(sql)
        except Exception as e:
            _ = e
            print(e)
            db.session.rollback()
            return json_response(message="数据修改失败", status=500)
        else:
            db.session.commit()
            return json_response(message="ok")

    @user_required
    @use_kwargs({
        # "data_id": fields.String(required=True, validate=valid_uuid),
        # TODO 临时关掉验证 不然之前的id删不掉
        "data_id": fields.String(required=True),
    })
    def delete(self, entity_id: str, data_id: str):
        """页面某一块section数据-修改

          ---
          tags:
            - page页面数据
          parameters:
            - name: entity_id
              in: path
              type: string
              required: true
              enum: ['12363708151a46879f3efb76780c5ba9']
              description: 实例id
            - name: data_id
              in: path
              type: string
              required: true
              enum: ['12363708151a46879f3efb76780c5ba9']
              description: 要修改的数据id
            - name: org_id
              in: querystring
              type: string
              required: false
              description: 组织id
          responses:
            200:
              description:  成功
              examples:
                response: {"message": "ok"}
        """
        try:
            table_name, condition = self.get_table_name(entity_id, data_id=data_id)
        except Exception as e:
            _ = e
            return json_response(message=str(e), status=404)
        delete_sql = "DELETE FROM %s WHERE %s" % (table_name, condition)
        try:
            db.session.execute(delete_sql)
            db.session.commit()
        except Exception as e:
            _ = e
            return json_response(message="数据操作失败%s" % (str(e)), status=500)
        return json_response(message="删除成功")

    @staticmethod
    def get_table_name(entity_id, data_id=None):
        entity_query_result = db.session.query(Entity.table_name) \
            .filter(Entity.id == entity_id) \
            .first()
        assert entity_query_result, "找不到对应的表"
        table_name = entity_query_result[0]
        condition = None
        if data_id:
            condition = "id='%s'" % data_id
            query_sql = "SELECT id FROM %s WHERE id=:id;" % table_name
            data_query_result = db.session.execute(query_sql, {"id": data_id}).fetchone()
            assert data_query_result, "找不到改数据"

        return table_name, condition

    @staticmethod
    def verify_field(entity_id, data, table_name, data_id=''):
        # 默认
        message = 'ok'
        status = 0
        # 检验数据
        entity_fields_verify = EntityField.query.filter_by(entity_id=entity_id).all()
        for field in entity_fields_verify:
            field_key = field.key
            # 验证类型
            verify_require = field.verify_require
            verify_only = field.verify_only
            verify_max = field.verify_max
            verify_min = field.verify_min
            verify_pattern = field.verify_pattern

            if verify_require and field_key not in data.keys():
                # TODO 先在前端验证
                print(field_key, 'require')
                continue
            # 唯一
            if verify_only and field_key in data.keys():
                verify_value = data[field_key]
                verify_sql = "SELECT 1 FROM %s WHERE %s = '%s'" % (table_name, field_key, verify_value)
                # 编辑的时候跳过判断自己
                if data_id:
                    verify_sql += " AND id != '%s'" % data_id
                query_result = db.session.execute(verify_sql).fetchone()
                if query_result:
                    print(field_key, verify_value, 'not only')
                    # return json_response(message="%s要求唯一, 已经存在%s" % (field_key, verify_value), status=409)
                    message = "%s要求唯一, 已经存在%s" % (field_key, verify_value)
                    status = 409
                    return message, status
        return message, status


class EntityOptionResource(Resource):
    @user_required
    @use_kwargs({
        'org_id': fields.String()
    })
    def get(self, entity_id, **kwargs):
        """修改业数据回显选项列表
          ---
          tags:
            - page页面数据
          parameters:
            - name: entity_id
              in: path
              type: string
              required: true
              enum: ['12363708151a46879f3efb76780c5ba9']
              description: 实例id
            - name: org_id
              in: querystring
              type: string
              required: false
              description: 组织id
          responses:
            200:
              description:  成功
              examples:
                response: {"data": {"entity_data": [], "entity_fields": []}}
        """
        entity = Entity.query.filter_by(id=entity_id).first()
        org_id = kwargs.get('org_id')
        if not entity:
            return json_response(message="未找到对应的entity", status=404)
        try:
            entity_schema = EntityOptionSchema(org_id=org_id)
            data = entity_schema.dump(entity).data
        except Exception as e:
            _ = e
            return json_response(message=str(e), status=403)
        return json_response(data=data)


class EntityResource(Resource):
    @user_required
    def get(self, entity_key):
        entity = Entity.query.filter(Entity.key == entity_key).first()
        if not entity:
            return json_response(message="未找到对应的entity", status=404)
        try:
            entity_schema = EntityFieldsSchema()
            data = entity_schema.dump(entity).data
        except Exception as e:
            _ = e
            return json_response(message=str(e), status=403)
        return json_response(data=data)


class EntityDataResource(Resource):
    @user_required
    @use_kwargs({
        'search_params': fields.List(fields.Dict()),
        'page_params': fields.List(fields.Dict()),
        'order_params': fields.List(fields.Dict())
    })
    def post(self, id, **kwargs):
        """修改业数据回显选项列表
          ---
          tags:
            - page页面数据
          parameters:
            - name: search_params
              in: data
              type: List
              required: false
              description: 列表搜索条件
            - name: page_params
              in: data
              type: List
              required: false
              description: 分页条件
            - name: order_params
              in: data
              type: List
              required: false
              description: 排序条件
          responses:
            200:
              description:  成功
              examples:
                response: {"data": {"entity_data": [], "entity_fields": []}}
        """
        entity = Entity.query.filter(Entity.id == id).first()
        if not entity:
            return json_response(message="未找到对应的entity", status=404)
        # try:
        entity_schema = EntitySchema()
        data = entity_schema.dump(entity).data
        # except Exception as e:
        #     _ = e
        #     return json_response(message=str(e), status=403)
        return json_response(data=data)
