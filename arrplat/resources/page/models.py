from sqlalchemy import Column, Integer, \
    ForeignKey, VARCHAR, Text, Boolean, JSON, BigInteger
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import backref

from extensions import db
from arrplat.common.utils import generate_uuid
import json


class Page(db.Model):
    direction_type_enum = {
        1: 'row',
        2: 'column'
    }
    __tablename__ = 'page'
    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    title = Column(VARCHAR(32), comment='标题')
    type = Column(TINYINT, comment='1:PC, 2:Mobile 页面类型')
    direction = Column(TINYINT, comment='1:row, 2:column 数据类型')
    # application_menu_id = Column(VARCHAR(32), ForeignKey('application_menus.id', ondelete='CASCADE'), comment='应用页面ID')
    application_id = Column(VARCHAR(32), ForeignKey('application.id', ondelete='CASCADE'), comment='应用页面ID')
    unique_id = Column(VARCHAR(32), default=generate_uuid)
    key = Column(VARCHAR(32), unique=True)
    params = Column(VARCHAR(200), comment='页面参数列表 数据为[]')

    @classmethod
    def direction_type_to_string(cls, direction_type: int) -> str:
        assert direction_type in cls.direction_type_enum, '没有对应的direction类型'
        return cls.direction_type_enum[direction_type]

    @classmethod
    def string_to_direction_type(cls, data_string: str) -> int:
        for k, v in cls.direction_type_enum.items():
            if data_string == v:
                return k


class PageSectionTab(db.Model):
    __tablename__ = 'page_section_tab'
    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    title = Column(VARCHAR(32), comment='标题')
    from_page_section_id = Column(VARCHAR(32), ForeignKey('page_section.id', ondelete='CASCADE'), comment='父组件', primary_key=True)
    to_page_section_id = Column(VARCHAR(32), ForeignKey('page_section.id', ondelete='CASCADE'), comment='子组件', primary_key=True)
    # entity_id = Column(VARCHAR(32), ForeignKey('entity.id', ondelete='CASCADE'), comment='实例ID')


class PageSection(db.Model):
    section_type_enum = {
        1: 'page',
        2: 'tab',
        3: 'details',
        4: 'form',
        5: 'search',
        6: 'html',
        7: 'buttons',
        8: 'search_buttons',
        9: 'list',
        10: 'analysis',
        11: 'editor'
    }
    __tablename__ = 'page_section'
    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    title = Column(VARCHAR(32), comment='标题')
    entity_id = Column(VARCHAR(32), ForeignKey('entity.id', ondelete='CASCADE'), comment='实例ID')
    entity_params = Column(VARCHAR(300), comment='查询实体的参数')
    page_id = Column(VARCHAR(32), ForeignKey('page.id', ondelete='CASCADE'), comment='页面ID')
    html_content = Column(Text, comment='页面内容')
    section_type = Column(TINYINT, comment='组件类型')
    has_add_btn = Column(Boolean, default=False, comment='是否显示添加按钮')
    nodes = Column(JSON, comment='Page Section 中的所有节点')
    sort = Column(Integer)
    create_time = Column(BigInteger, comment='创建时间')

    page = db.relationship(Page, backref=backref('page_section', order_by=sort))
    entity = db.relationship('Entity', backref='page_section')

    page_section_to = db.relationship('PageSectionTab', backref=backref('to', uselist=False), primaryjoin=id == PageSectionTab.to_page_section_id, lazy='dynamic', uselist=True)
    page_section_from = db.relationship('PageSectionTab', backref=backref('from', uselist=False), primaryjoin=id == PageSectionTab.from_page_section_id, lazy='dynamic', uselist=True)

    @classmethod
    def section_type_to_string(cls, section_type: int) -> str:
        assert section_type in cls.section_type_enum, '没有对应的page类型'
        return cls.section_type_enum[section_type]

    @classmethod
    def string_to_data_type(cls, data_string: str) -> int:
        for k, v in cls.section_type_enum.items():
            if data_string == v:
                return k


class Entity(db.Model):
    data_type_enum = {
        1: 'db_table',  # 从sql字段的表中查询
        2: 'analysis',  #
        3: 'sql'  # 使用sql字段的SQL进行查询
    }
    __tablename__ = 'entity'
    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    title = Column(VARCHAR(32), comment='标题')
    table_name = Column(VARCHAR(32), unique=False, comment='表名')
    query_sql = Column(Text, comment='sql语句')
    data_type = Column(TINYINT, comment='数据类型')
    key = Column(VARCHAR(32), unique=True)
    has_connect_org = Column(Boolean, default=True,  comment='是否通过 org_id 与 组织体系链接')

    @classmethod
    def data_type_to_string(cls, data_type: int) -> str:
        assert data_type in cls.data_type_enum, '没有对应的data_type类型'
        return cls.data_type_enum[data_type]

    @classmethod
    def string_to_data_type(cls, data_string: str) -> int:
        for k, v in cls.data_type_enum.items():
            if data_string == v:
                return k


class EntityField(db.Model):
    data_type_enum = {          # 展示页面字段数据类型
        1: 'string',                # 字符串
        2: 'number',                # 数值
        3: 'rich_text',             # 富文本
        4: 'date',                  # 日期类型
        5: 'date_down',             # 倒计时
        6: 'price',                 # 价格
        7: 'enum',
        8: 'dict',                  # 字典类型 关联 dict_list 字段
        9: 'datetime',              # 日期时间类型
        11: 'time',                 # 时间类型
        12: 'list',                 # 列表 (根据 query_sql 字段 查出的数据展示)
        13: 'key_value',            # 键值对 (根据 query_sql 字段 查出的数据展示)
        14: 'switch',
        15: 'boolean',              # Boolean 类型 展示页面显示：是/否 修改页面为 switch 开关
        16: 'global-component',     # 数据修改时使用前端全局组件
        17: 'foreign-key',          # 外键 修改时，根据 data_source_sql 获取下拉框参数
        18: 'text-area',          # 多行文本框
    }

    foreign_type_enum = {
        1: 'one-to-one',  # 数据修改时使用前端全局组件
        2: 'many-to-many',  # 外键 修改时，根据 data_source_sql 获取下拉框参数
        3: 'one-to-many',  # Boolean 类型 展示页面显示：是/否 修改页面为 switch 开关
        4: 'many-to-one',  # 数据修改时使用前端全局组件
    }

    display_type_enum = {     # 展示页面字段数据类型
        1: 'auto',              # 根据 data_type 及其他配置自动展示数据
        2: 'global-component',  # 展示时使用前端全局组件
        3: 'iframe',            # 展示时使用 iframe
    }

    type_enum = {
        1: 'value',             # 代表该entity field 为 entity 的表/sql 中的一个字段，关联 key
        2: 'buttons',           # 该字段为按钮组
        3: 'sql',               # 该字段为单独的sql 关联 query_sql 字段
    }

    __tablename__ = 'entity_field'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)

    # 基本信息
    type = Column(TINYINT, comment='是否是数据或者是按钮')
    entity_id = Column(VARCHAR(32), ForeignKey('entity.id', ondelete='CASCADE'))
    key = Column(VARCHAR(32))
    table_name = Column(VARCHAR(32), comment='字段属于哪张实体表')
    name = Column(VARCHAR(32))
    is_primary = Column(Boolean, default=False, comment='是否是主键')
    default_value = Column(VARCHAR(200), comment='默认值')
    description = Column(VARCHAR(200), comment='字段描述')

    # 数据信息
    data_type = Column(TINYINT, comment='数据类型')
    dict_list = Column(VARCHAR(300))
    query_sql = Column(Text, comment='sql语句')
    data_source_sql = Column(Text, comment='数据源SQL 当 data_type 为 foreign-key 时在该字段获取编辑页面数据')

    # 展示信息
    display_type = Column(TINYINT, comment='字段生成类型')
    form_component = Column(VARCHAR(50), comment='表单自定义组件')
    display_component = Column(VARCHAR(50), comment='展示自定义组件')
    sort = Column(Integer)
    exists_type = Column(Text, comment='在哪些页面显示')

    # Field link
    has_link = Column(Boolean, default=False, comment='展示数据是否有跳转链接')
    link_address = Column(VARCHAR(300), comment='has_link 为 True 时，跳转页面的链接，后接 ${field_key} 填充参数')
    link_button_id = Column(VARCHAR(32), ForeignKey('button.id', ondelete='CASCADE'), comment='如果连接是个按钮（有额外的类型和参数）')

    has_sort = Column(Boolean, default=False)
    has_search = Column(Boolean, default=False)

    # 外键信息
    foreign_type = Column(TINYINT, comment='外键类型 eg. 一对一、一对多...')
    foreign_table_name = Column(VARCHAR(32), comment='外键表表名')
    foreign_their_key = Column(VARCHAR(32), comment='外键表字段名')
    foreign_our_key = Column(VARCHAR(32), comment='本表在外键表的字段名')

    # 表单验证
    verify_pattern = Column(VARCHAR(100), comment='表单验证的正则表达式')
    verify_require = Column(Boolean, default=False, comment='必填')
    verify_only = Column(Boolean, default=False, comment='唯一')
    verify_max = Column(TINYINT, default=-1, comment='最大数值')
    verify_min = Column(TINYINT, default=-1, comment='最小数值')

    entity = db.relationship('Entity', backref=backref('entity_fields', cascade='all,delete', lazy='dynamic', order_by=sort))

    @classmethod
    def format(cls, data):
        data_type = data.get('data_type')
        foreign_type = data.get('foreign_type')
        if data_type:
            data['data_type'] = EntityField.data_type_to_string(data_type)

        if foreign_type:
            data['foreign_type'] = EntityField.foreign_type_to_string(foreign_type)

        if data.get('dict_list'):
            data['dict_list'] = json.loads(data.get('dict_list'))

    @staticmethod
    def converter(field, entity_id, sort=0):
        is_primary = field.get('is_primary', False)
        key = field.get('key')
        name = field.get('name')
        data_type = field.get('data_type')
        display_type = field.get('display_type')
        value_type = field.get('type')

        has_link = field.get('has_link', False)
        link_address = field.get('link_address')
        # link_button_id = field.get('link_button_id')
        # link_button_id = db.relationship('Button', backref=backref('entity_field_button', lazy='dynamic'))

        has_sort = field.get('has_sort', False)
        has_search = field.get('has_search', False)
        exists_type = field.get('exists')
        form_component = field.get('form_component')
        display_component = field.get('display_component')
        sql = field.get('sql')
        data_source_sql = field.get('data_source_sql')
        dict_list = field.get('dict_list', [])
        description = field.get('description')
        default_value = field.get('default_value')

        foreign_type = field.get('foreign_type')
        foreign_table_name = field.get('foreign_table_name')
        foreign_their_key = field.get('foreign_their_key')
        foreign_our_key = field.get('foreign_our_key')

        verify_pattern = field.get('verify_pattern')
        verify_require = field.get('verify_require', False)
        verify_only = field.get('verify_only', False)
        verify_max = field.get('verify_max', -1)
        verify_min = field.get('verify_min', -1)

        return EntityField(
            form_component=form_component,
            display_component=display_component,
            is_primary=is_primary,
            entity_id=entity_id,
            key=key,
            name=name,
            data_type=EntityField.string_to_data_type(data_type),
            display_type=EntityField.string_to_display_type(display_type),
            type=EntityField.string_to_type(value_type),
            dict_list=json.dumps(dict_list),
            sort=sort,
            link_address=link_address,
            data_source_sql=data_source_sql,
            has_link=1 if has_link else 0,
            has_sort=1 if has_sort else 0,
            has_search=1 if has_search else 0,
            query_sql=sql,
            exists_type=''.join([i + ',' for i in exists_type]) if exists_type else '',
            foreign_type=EntityField.string_to_foreign_type(foreign_type),
            foreign_table_name=foreign_table_name,
            foreign_their_key=foreign_their_key,
            foreign_our_key=foreign_our_key,

            description=description,
            default_value=default_value,

            verify_pattern=verify_pattern,
            verify_require=1 if verify_require else 0,
            verify_only=1 if verify_only else 0,
            verify_max=verify_max,
            verify_min=verify_min
        )

    @classmethod
    def foreign_type_to_string(cls, foreign_type: int) -> str:
        assert foreign_type in cls.foreign_type_enum, '没有对应的foreign_type类型'
        return cls.foreign_type_enum[foreign_type]

    @classmethod
    def data_type_to_string(cls, data_type: int) -> str:
        assert data_type in cls.data_type_enum, '没有对应的data_type类型'
        return cls.data_type_enum[data_type]

    @classmethod
    def display_type_enum_to_string(cls, display_type: int) -> str:
        assert display_type in cls.display_type_enum, '没有对应的display_type类型'
        return cls.display_type_enum[display_type]

    @classmethod
    def string_to_foreign_type(cls, foreign_type: int) -> str:
        for k, v in cls.foreign_type_enum.items():
            if foreign_type == v:
                return k

    @classmethod
    def string_to_display_type(cls, data_string: str) -> int:
        for k, v in cls.display_type_enum.items():
            if data_string == v:
                return k

    @classmethod
    def string_to_data_type(cls, data_string: str) -> int:
        for k, v in cls.data_type_enum.items():
            if data_string == v:
                return k

    @classmethod
    def type_enum_to_string(cls, _type: int) -> str:
        assert _type in cls.type_enum, '没有对应的type类型'
        return cls.type_enum[_type]

    @classmethod
    def string_to_type(cls, data_string: str) -> int:
        for k, v in cls.type_enum.items():
            if data_string == v:
                return k


class EntityFieldButton(db.Model):
    __tablename__ = 'entity_field_button'
    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    entity_field_id = Column(VARCHAR(32), ForeignKey('entity_field.id', ondelete='CASCADE'), comment='实例字段ID')
    button_id = Column(VARCHAR(32), ForeignKey('button.id', ondelete='CASCADE'), comment='按钮ID')

    entity_field = db.relationship('EntityField', backref=backref('entity_field_button', lazy='dynamic'))
    button = db.relationship('Button', backref=backref('entity_field_button', lazy='dynamic'))


class Button(db.Model):
    button_type_enum = {
        1: 'edit',
        2: 'delete',
        4: 'details',
        5: 'add',
        6: 'link',
        7: 'action',
        8: 'dialog-list',
        9: 'dialog-details',
    }
    __tablename__ = 'button'
    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(32))
    button_type = Column(TINYINT, comment='button类型')
    link = Column(VARCHAR(300), comment='跳转页面链接')
    entity_key = Column(VARCHAR(32), comment='如果button type 为 dialog-* 则使用该字段连接 entity')
    entity_params = Column(VARCHAR(302), comment='如果button type 为 dialog-* 时 对 entity 的参数')

    @classmethod
    def type_to_string(cls, button_type: int) -> str:
        assert button_type in cls.button_type_enum, '没有对应的button类型'
        return cls.button_type_enum[button_type]

    @classmethod
    def string_to_button_type(cls, data_string: str) -> int:
        for k, v in cls.button_type_enum.items():
            if data_string == v:
                return k

    @staticmethod
    def converter(obj):
        name = obj.get('name')
        button_type = obj.get('type')
        link = obj.get('link')
        return Button(
            name=name,
            link=link,
            button_type=Button.string_to_button_type(button_type)
        )
