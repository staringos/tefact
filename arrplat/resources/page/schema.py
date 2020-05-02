import re
import json

from flask import request
from marshmallow import fields, post_dump, pre_dump

from .services import entity_data_search, entity_data_pagination, entity_data_sort, \
    entity_data_execute, entity_data_connect_org, entity_init_sql, entity_data_params
from arrplat.resources.page.models import Page, PageSection, PageSectionTab, Entity, EntityField
from arrplat.config import DEFAULT_PAGE, DEFAULT_PAGE_SIZE
from extensions import ma, db


class EntityFieldSchema(ma.ModelSchema):

    @post_dump
    def format_data_type(self, data):
        return EntityField.format(data)

    class Meta:
        model = EntityField


class EntitySchema(ma.ModelSchema):
    entity_fields = fields.Nested(EntityFieldSchema, many=True)
    page_section = fields.Nested('PageSectionSchema')

    button_sql = 'SELECT DISTINCT b.* FROM  button b JOIN entity_field_button efb ON b.id=efb.button_id AND efb.entity_field_id in :entity_field_id JOIN entity_field ef ON efb.entity_field_id=ef.id;'

    def __init__(self, search_condition=None, is_all=False, *args, **kwargs):
        super(EntitySchema, self).__init__(*args, **kwargs)
        self.search_condition = search_condition
        self.is_all = is_all
        self.sql_params = dict()
        self.entity_params = dict()
        self.query_sql = ''
        self.page_sql = ''
        self.query_one = False
        self.query_form_data = dict()
        self.is_analysis = False
        self.page_section_type = 0

        self.entity_field_list = list()
        self.button_entity_field_list = list()
        self.sql_entity_field_list = list()
        self.foreign_entity_field_list = list()

    @pre_dump
    def format_sql(self, obj):
        self.query_form_data = obj.query_form_data if hasattr(obj, 'query_form_data') else dict()
        search_params = self.query_form_data.get('search_condition')
        detail_params = self.query_form_data.get('detail_condition')
        self.page_section_type = obj.page_section_type
        self.entity_params = obj.entity_params

        # 跳过data_type为analysis的
        if obj.data_type == 2 or not obj.table_name:
            print(obj.key, 'obj.data_type == 2 or not obj.table_name')
            # 如果这里不设置query_sql, 之后execute_query_sql方法会判断跳过, 需要设置is_analysis = True
            self.is_analysis = True
            return

        search_params = entity_data_connect_org(search_params, obj.table_name, obj.has_connect_org)

        print('entity:key:', obj.key)

        self.query_sql = entity_init_sql(obj.query_sql, obj.table_name)
        self.query_sql = entity_data_search(self, self.query_sql, search_params, detail_params, obj.table_name)
        # entity_params
        self.query_sql = entity_data_params(self, self.query_sql, obj.table_name)
        self.query_sql = entity_data_sort(self, self.query_sql, obj.table_name)
        self.page_sql = self.get_page_sql(query_sql=self.query_sql)
        self.query_sql = entity_data_pagination(self, self.query_sql)

    @post_dump(pass_many=True)
    def execute_query_sql(self, data, many, **kwargs):
        data['entity_data'] = list()
        # 有查询语句或者查询数据
        if self.query_sql or self.is_analysis:
            entity_data_execute(self, data)

        self.delete_query_sql(data['entity_fields'])
        del data['query_sql']
        del data['table_name']
        self.reset_attr()
        return data

    def reset_attr(self):
        """重置属性"""
        self.sql_params.clear()
        self.query_form_data.clear()
        self.entity_field_list.clear()
        self.button_entity_field_list.clear()
        self.sql_entity_field_list.clear()
        self.query_one = False
        self.query_sql = ''

    @staticmethod
    def delete_query_sql(array: list):
        for item in array:
            if item.get('query_sql'):
                del item['query_sql']

    @staticmethod
    def get_page_sql(query_sql: str):
        page_sql = re.sub('^select .*? from', 'select count(1) as total_count from', query_sql.strip().lower())
        return page_sql

    def get_page_size(self):
        page = self.query_form_data['page']['page'] if self.query_form_data.get('page') else DEFAULT_PAGE
        size = self.query_form_data['page']['size'] if self.query_form_data.get('page') else DEFAULT_PAGE_SIZE
        return page, size

    @staticmethod
    def format_entity_field_data(cursor, entity_field_data):
        data_type = entity_field_data.get('data_type')
        if data_type == 'key_value':
            temp = cursor.fetchone()
            field_data = dict(temp) if temp else None
        elif data_type == 'list':
            field_data = [dict(query_item) for query_item in cursor.fetchmany()]
        else:
            temp = cursor.fetchone()
            field_data = temp[0] if temp else None
        return field_data

    class Meta:
        model = Entity
        exclude = ('page_section',)


class PageSectionSchema(ma.ModelSchema):
    entity = fields.Nested(EntitySchema, exclude=('page_section',))

    def __init__(self, page=None, search_condition=None, sort=None, *args, **kwargs):
        super(PageSectionSchema, self).__init__(*args, **kwargs)
        self.page = page if page else {'page': DEFAULT_PAGE, 'size': DEFAULT_PAGE_SIZE}
        self.search_condition = search_condition
        self.sort = sort

    @pre_dump
    def get_condition_entity(self, obj):
        query_form_data = {
            'page': self.page,
            'search_condition': self.search_condition,
            'sort': self.sort
        }
        if hasattr(obj, 'detail_params'):
            try:
                entity_params = str(obj.entity_params)
                for key, value in obj.detail_params.items():
                    query_form_data['detail_condition'] = entity_params.replace('${%s}' % key, '"%s"' % value)
            except Exception as e:
                raise Exception('page—section中的entity_param不是字符串,%s' % str(e))

        if obj.entity:
            if hasattr(obj, 'entity_params'):
                entity_params = str(obj.entity_params)
                setattr(obj.entity, 'entity_params', entity_params)

            setattr(obj.entity, 'query_form_data', query_form_data)
            setattr(obj.entity, 'page_section_type', obj.section_type)

    class Meta:
        model = PageSection
        fields = (
            'id', 'title', 'entity', 'html_content', 'section_type', 'page_section_to',
            'has_add_btn', 'entity_params', 'nodes')


class PageSectionTabSchema(ma.ModelSchema):
    class Meta:
        model = PageSectionTab


class PageSchema(ma.ModelSchema):
    page_section = fields.Nested(PageSectionSchema, many=True, exclude=('page',))

    @pre_dump
    def set_condition(self, obj):
        if hasattr(obj, 'page_section'):
            try:
                params_list = json.loads(obj.params)
            except Exception as e:
                _ = e
                params_list = []
            args = request.args
            org_id = args.get('org_id')
            if params_list and len(params_list) <= len(args):
                temp_params = dict()
                for key in params_list:
                    if not args.get(key):
                        if org_id:
                            return
                        raise Exception('详情所需的参数太少')
                    temp_params[key] = args.get(key)

                for page_section in obj.page_section:
                    setattr(page_section, 'detail_params', temp_params)

    class Meta:
        model = Page
        fields = ('id', 'title', 'type', 'direction', 'key', 'application_id', 'unique_id', 'page_section')


class PageDetailsSchema(PageSchema):
    class Meta:
        model = Page
        fields = ('id', 'title', 'type', 'direction', 'key', 'application_id', 'unique_id', 'page_section')


class EntityOptionSchema(ma.ModelSchema):
    entity_fields = fields.Nested(EntityFieldSchema, many=True)

    def __init__(self, org_id=None, *args, **kwargs):
        super(EntityOptionSchema, self).__init__(*args, **kwargs)
        self.org_id = org_id

    @post_dump(pass_many=True)
    def execute_query_sql(self, data, many, **kwargs):
        temp = dict()
        for item in data.get('entity_fields', list()):
            is_foreign_key = item.get('data_type') == 'foreign-key' and item.get('data_source_sql')

            if not item.get('query_sql') and not is_foreign_key:
                continue

            if item.get('query_sql'):
                query_sql = self.remove_condition(item['query_sql'])

            if is_foreign_key:
                query_sql = item.get('data_source_sql')

            if self.org_id and query_sql.find('org_id') != -1:
                query_sql += (' where org_id="%s"' % self.org_id) if query_sql.find('where') > -1 else (
                    ' and org_id="%s"' % self.org_id)

            key = item.get('key', '')
            entity_field_data = db.session.execute(query_sql).fetchall()

            temp[key] = [dict(_) for _ in entity_field_data]

        return temp

    @staticmethod
    def remove_condition(query_sql: str):
        query_sql = re.sub('where.*', '', query_sql.lower())
        return query_sql

    class Meta:
        model = Entity
        exclude = ('page_section',)


class EntityFieldsSchema(ma.ModelSchema):
    entity_fields = fields.Nested(EntityFieldSchema, many=True)

    class Meta:
        model = Entity
