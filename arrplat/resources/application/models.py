from sqlalchemy import Column, Integer, \
    ForeignKey, DateTime, BigInteger, VARCHAR, Text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship, backref
from marshmallow import fields, post_dump
from extensions import db
from arrplat.common.utils import generate_uuid, get_timestamp
from arrplat.resources.organization.models import Organization


class Application(db.Model):
    type_enum = {
        0: 'default',
        1: 'third',
        2: 'light',
    }
    __tablename__ = 'application'
    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(32), nullable=False, unique=True, comment='官方唯一的名')
    title = Column(VARCHAR(32), nullable=True, comment='不唯一的名')
    type = Column(TINYINT, nullable=False, default=type_enum[1], comment='应用类型 1 第三方应用 2 轻应用')
    description = Column(Text)
    official_website = Column(Text, comment='应用官方地址')
    install_number = Column(Integer, default=0)
    version = Column(VARCHAR(32))
    icon = Column(Text, comment='icon')
    head_image = Column(Text, comment='头像')
    visible = Column(TINYINT, comment='是否可用')
    deletable = Column(TINYINT, comment='是否可删除')
    is_official = Column(TINYINT, comment='是否是官方的')
    images = Column(Text, comment='应用介绍图片')
    sort = Column(Integer, comment='app排序')
    api_route = Column(VARCHAR(128), comment='api路由')
    admin_route = Column(VARCHAR(128), comment='admin路由')
    create_time = Column(BigInteger, default=get_timestamp)
    application_category_id = Column(VARCHAR(32), ForeignKey('application_category.id'), comment='应用类别')
    unique_id = Column(VARCHAR(32), default=generate_uuid)
    key = Column(VARCHAR(32), unique=True, comment='应用的唯一命名')
    own_org_id = Column(VARCHAR(32), comment='轻应用的拥有组织ID')

    @classmethod
    def format(cls, data):
        data['type'] = cls.type_enum[data.get('type')]


class OrgApplication(db.Model):
    __tablename__ = 'org_application'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    organization_id = Column(VARCHAR(32), ForeignKey('organization.id', ondelete="CASCADE"), comment='组织id')
    application_id = Column(VARCHAR(32), ForeignKey('application.id', ondelete="CASCADE"), comment='应用id')
    expire_date = Column(DateTime)
    status = Column(TINYINT, comment='是否启用')

    application = relationship('Application', backref=backref('org_application', cascade='all,delete'), lazy='select')
    organization = relationship(Organization, backref=backref('org_application', cascade='all,delete'), lazy='select')


class ApplicationMenus(db.Model):
    page_type_enum = {
        1: 'customer',
        2: 'page',
    }
    __tablename__ = 'application_menus'
    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    application_id = Column(VARCHAR(32), ForeignKey('application.id', ondelete='CASCADE'), comment='应用id')
    name = Column(VARCHAR(32), comment='菜单名称')
    icon = Column(Text, comment='小图标路径')
    link = Column(Text, comment='菜单的链接')

    type = Column(TINYINT, default=1, comment='页面类型 .. 1:customer 2:page')
    page_key = Column(VARCHAR(32))
    unique_id = Column(VARCHAR(32), default=generate_uuid)
    platform = Column(VARCHAR(32), default='PC', comment='菜单所属平台，.. => pc,mobile')
    sort = Column(Integer, default=0, comment='排序')
    parent_id = Column(VARCHAR(32), default='0', comment='父id')
    page_id = Column(VARCHAR(32), ForeignKey('page.id'), comment='页面id')

    application = relationship('Application', backref=backref('menus', lazy='dynamic', cascade='all, delete-orphan',
                                                              passive_deletes=True))
    page = relationship('Page', backref=backref('application_menus'), uselist=False)

    @classmethod
    def page_type_to_string(cls, page_type: int) -> str:
        assert page_type in cls.page_type_enum, '没有对应的data_type类型'
        return cls.page_type_enum[page_type]

    @classmethod
    def string_to_page_type(cls, page_type_string: str) -> int:
        for k, v in cls.page_type_enum.items():
            if page_type_string == v:
                return k


class Message(db.Model):
    __tablename__ = 'message'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    title = Column(VARCHAR(128))
    content = Column(Text)
    send_time = Column(BigInteger)
    read_time = Column(BigInteger)
    is_read = Column(TINYINT, comment='是否已读(0. 否 1. 是)', default=0)
    message_type = Column(TINYINT, comment='消息类型(1. system系统 2. plus插件 3. org组织 4. invitee邀请)')
    application_id = Column(VARCHAR(32), ForeignKey('application.id', ondelete='CASCADE'), comment='应用id')
    organization_id = Column(VARCHAR(32), ForeignKey('organization.id', ondelete='CASCADE'), comment='组织id')
    user_id = Column(VARCHAR(32), ForeignKey('user.id', ondelete='CASCADE'), comment='员工id')

    user = relationship('User', backref=backref('message'))


class ApplicationCategory(db.Model):
    __tablename__ = 'application_category'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(32), comment='类别名')
    application_category = relationship('Application', backref=backref('application_category'))
