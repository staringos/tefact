from arrplat.config import DEFAULT_PAGE, DEFAULT_PAGE_SIZE
from flask import request
import copy
from arrplat.common.utils import calculate_page, get_sql_params
from .models import DataSource, Page
from extensions import db
from arrplat.resources.organization.services import org_exists
from arrplat.resources.organization.models import OrgStaff
from arrplat.resources.application.models import Application
from arrplat.common.utils import json_response


def allow_access_page(id, user_id):
    if not id:
        return json_response(message="参数错误", status=400)

    page = db.session.query(Page, Application.own_org_id)\
        .join(Application, Page.application_id == Application.id)\
        .filter(Page.id == id)\
        .first()

    if not page:
        return json_response(message=f"页面未找到", status=404)

    org_id = page[1]
    staff = db.session.query(OrgStaff).filter(OrgStaff.user_id == user_id and OrgStaff.org_id == org_id).first()

    if not staff:
        return json_response(message=f"用户无权限", status=403)

    return page[0], org_id


def split_different_field(self, fields):
    for item in fields:
        if item['type'] == 2:  # Button
            self.button_entity_field_list.append(item['id'])
        elif item['type'] == 3 and item['query_sql'] and item['query_sql'].find(item['key']) == -1:
            # 不严谨
            pass
        else:
            self.entity_field_list.append(item['key'])

        if item['type'] == 3:  # SQL
            self.sql_entity_field_list.append(item)

        # 关联表字段跳过
        if item['data_type'] == 'foreign-key' and item['foreign_type'] == 'many-to-many':
            self.entity_field_list.remove(item['key'])
            # 关联查询
            self.foreign_entity_field_list.append(item)


def loop_sql_entity_field(self, item):
    for sql_item in self.sql_entity_field_list:
        key = sql_item.get('key')
        # TODO 为何是not key not in item.values()?
        if not sql_item.get('query_sql') or not key not in item.values():
            continue
        query_sql = sql_item.get('query_sql', '')
        sql_params = get_sql_params(query_sql)
        # 判断sql是否正确标识
        value_flag = True
        for param in sql_params:
            value = item[param] if item.get(param) else ''
            if not value:
                value_flag = False
                break
            query_sql = query_sql.replace('${%s}' % param, '"%s"' % value)
        # value_flag = False sql有问题 无法执行
        if value_flag:
            cursor = db.session.execute(query_sql)
            field_data = self.format_entity_field_data(cursor, sql_item)
            item[key] = field_data
            # del sql_item['query_sql']


def entity_init_sql(sql, table_name):
    if sql:
        return sql

    return 'select * from %s' % table_name


def entity_data_execute(self, data):
    # 先判断section_type, 3: 'details', 9: 'list', 10: 'analysis',
    # 列表数据
    if self.page_section_type == 9:
        split_different_field(self, data.get('entity_fields', list()))

        self.query_sql = self.query_sql.replace('*', ', '.join(self.entity_field_list))
        button_row_proxy_list = None
        if self.button_entity_field_list:
            button_row_proxy_list = db.session \
                .execute(self.button_sql, {'entity_field_id': self.button_entity_field_list}).fetchall()
        entity_row_proxy_list = db.session.execute(self.query_sql, self.sql_params).fetchall()
        page_row_proxy = db.session.execute(self.page_sql, self.sql_params).fetchone()

        total_count = page_row_proxy[0] if page_row_proxy else 0
        button_list = [dict(item) for item in button_row_proxy_list] if button_row_proxy_list else []

        for _ in entity_row_proxy_list:
            item = dict(_)
            item['options'] = button_list
            loop_sql_entity_field(self, item)

            # 补充多对多关联表数据
            if self.foreign_entity_field_list:
                # TODO 单独的查询语句可能没有id
                item_id = item['id']
                for field in self.foreign_entity_field_list:
                    field_key = field['key']
                    foreign_table_name = field['foreign_table_name']
                    foreign_our_key = field['foreign_our_key']
                    foreign_their_key = field['foreign_their_key']
                    sql_query_foreign = " SELECT %s,%s FROM %s WHERE %s = '%s' " % (
                        foreign_our_key, foreign_their_key, foreign_table_name, foreign_our_key, item_id)
                    fs = db.session.execute(sql_query_foreign).fetchall()
                    fs_list = []
                    for f in fs:
                        fs_list.append(f[foreign_their_key])
                    item[field_key] = fs_list
            data['entity_data'].append(item)
        page, size = self.get_page_size()
        data['page'] = calculate_page(total_count=total_count, page=page, page_size=size)

    # detail
    if self.page_section_type == 3:
        split_different_field(self, data.get('entity_fields', list()))
        self.query_sql = self.query_sql.replace('*', ', '.join(self.entity_field_list))
        entity_row_proxy = db.session.execute(self.query_sql, self.sql_params).fetchone()
        item = dict(entity_row_proxy)
        loop_sql_entity_field(self, item)

        # 补充多对多关联表数据
        item_id = item['id']
        for field in self.foreign_entity_field_list:
            field_key = field['key']
            foreign_table_name = field['foreign_table_name']
            foreign_our_key = field['foreign_our_key']
            foreign_their_key = field['foreign_their_key']
            sql_query_foreign = " SELECT %s,%s FROM %s WHERE %s = '%s' " % (
                foreign_our_key, foreign_their_key, foreign_table_name, foreign_our_key, item_id)
            fs = db.session.execute(sql_query_foreign).fetchall()
            fs_list = []
            for f in fs:
                fs_list.append(f[foreign_their_key])
            item[field_key] = fs_list
        data['entity_data'] = item

    # analysis
    elif self.page_section_type == 10:
        # 先判断analysis数据, data_type=2
        # 循环fields
        # 执行field里的query_sql
        if data.get('data_type') == 2 or not data.get('table_name'):
            data['entity_data'] = dict()
            entity_fields = data.get('entity_fields', [])
            for entity in entity_fields:
                key = entity.get('key', '')
                # name = entity.get('name', '')
                # sql_query_analysis = entity.get('query_sql', '')
                # TODO 替换参数
                sql_query_analysis = "select count(1) as `number` from edu_course where teacher_employee_id = 3 and course_type=2"
                analysis_data = db.session.execute(sql_query_analysis).fetchone()
                item_value = analysis_data[0] if analysis_data else 0
                data['entity_data'][key] = item_value
    else:
        print('error: not page_section_type', self.page_section_type)
        pass


def entity_data_connect_org(search_params, table_name, has_connect_org):
    if not has_connect_org:
        return

    # search_params: list, 之前是dict
    tmp_search_params = list()
    if search_params and isinstance(search_params, list):
        tmp_search_params = copy.deepcopy(search_params)
    # if search_params and 'value' in search_params.keys():
    #     search_params_dict = copy.deepcopy(search_params['value'])
    #     for k, v in search_params_dict.items():
    #         tmp_search_params.append({'field_name': k, 'value': v})

    try:
        if request.method == 'POST':
            org_id = request.json.get('org_id')
        else:
            org_id = request.args.get('org_id')
        assert org_id, '参数中未获取到组织id'
    except Exception as e:
        _ = e
        raise Exception('参数中未获取到组织id')

    org_data = {'field_name': 'org_id', 'value': org_id, 'table_name': table_name}
    tmp_search_params.append(org_data)

    return tmp_search_params


def entity_data_sort(self, sql, table_name):
    if not self.query_form_data.get('sort') and table_name:
        # 默认创建时间倒序
        # TODO 风险 如果表里没有create_time字段会报错
        sql += ' ORDER BY %s.create_time DESC ' % table_name
        return sql

    field_name = self.query_form_data['sort'].get('field_name', '')
    if field_name:
        order = self.query_form_data['sort'].get('order', 'asc').strip().lower()
        # 兼容万一传错了参数 默认asc
        if order not in ['asc', 'desc']:
            order = 'asc'
        sql += ' ORDER BY %s %s' % (field_name, order)
    return sql


def entity_data_pagination(self, sql):
    # TODO 没看懂, is_all 应该直接返回sql, 现在是not all 返回
    if self.is_all:
        return sql

    tmp_sql = sql

    if self.query_form_data.get('page'):
        page = self.query_form_data['page']['page']
        size = self.query_form_data['page']['size']
        tmp_sql += ' LIMIT %s OFFSET %s ' % (size, (page - 1) * size)
    else:
        tmp_sql += ' LIMIT %s OFFSET %s ' % (DEFAULT_PAGE_SIZE, (DEFAULT_PAGE - 1) * DEFAULT_PAGE_SIZE)
        self.query_form_data['page'] = {
            'page': DEFAULT_PAGE,
            'size': DEFAULT_PAGE_SIZE
        }

    return tmp_sql


def entity_data_search(self, sql, search_params, detail_params, base_table_name):
    # 小技巧, sql直接加上where 1=1 避免后续判断问题
    if sql and sql.upper().find(' WHERE ') == -1:
        sql += ' WHERE 1=1 '

    # TODO 没看懂之前的逻辑 为什么要return
    # if search_params:
    #     return sql

    tmp_sql = sql

    if self.search_condition and isinstance(self.search_condition, list):
        search_params.extend(self.search_condition)
    where_exist = True if detail_params else False
    # if not where_exist:
    #     tmp_sql += ' WHERE '
    temp = list()

    # search_params 应该为list 但是存在为None的情况
    if search_params:
        for item in search_params:
            # value是必填项
            if 'field_name' not in item.keys() or 'value' not in item.keys():
                continue
            table_name = item.get('table_name')
            if table_name and len(table_name) > 0:
                temp.append('%s.%s=:%s' % (table_name, item['field_name'], item['field_name']))
            else:
                # 如果没有table_name, 默认都加了base_table_name 不然字段会有歧义
                # 模糊查询
                if item.get('search_type', 0) == 1:
                    # q = " name like '%上地校区%' "
                    q = f" {base_table_name}.{item['field_name']} like '%{item['value'].strip()}%' "
                    temp.append(q)
                else:
                    temp.append('%s.%s=:%s' % (base_table_name, item['field_name'], item['field_name']))

            self.sql_params[item['field_name']] = item['value']
            if item['field_name'] == 'id':
                self.query_one = True

    if temp:
        if not where_exist:
            tmp_sql += ' and ' + ' and '.join(temp)
        else:
            tmp_sql += ' and %s' % (','.join(temp))

    return tmp_sql


# 解析entity_params
def entity_data_params(self, sql, table_name):
    entity_params = self.entity_params
    # 'id=${id}&name=${name}'
    if entity_params:
        entity_param_list = entity_params.split('&')
        for param_item in entity_param_list:
            # id=${id}
            param_key = param_item.split('=')[0].strip()
            param_value = request.args.get(param_key, '')
            if param_value:
                sql += (" and %s.%s = '%s' " % (table_name, param_key, param_value))

    return sql
