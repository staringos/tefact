from sqlalchemy import Column,\
    ForeignKey,  BigInteger, VARCHAR
from sqlalchemy.dialects.mysql import TINYINT

from arrplat.common.utils import generate_uuid
from extensions import db
from sqlalchemy.orm import relationship, backref


# 组织角色表
class OrgRoleConfig(db.Model):
    __tablename__ = 'org_role_config'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(128), comment='角色名')
    intro = Column(VARCHAR(128), comment='介绍')
    create_time = Column(BigInteger, comment='创建时间')
    org_id = Column(VARCHAR(32), ForeignKey('organization.id', ondelete='CASCADE'), comment='组织ID')


# 组织权限功能配置表
class OrgAuthPowerConfig(db.Model):
    __tablename__ = 'org_auth_power_config'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(128), comment='功能名')
    parent_id = Column(VARCHAR(32), ForeignKey('org_auth_power_config.id', ondelete='CASCADE'), comment='自关联的父级ID')
    icon = Column(VARCHAR(512), comment='菜单栏的icon')
    url = Column(VARCHAR(512), comment='菜单栏的跳转url')
    create_time = Column(BigInteger, comment='创建时间')
    type = Column(TINYINT, nullable=True, comment='权限所属类别(0: system 1: plugins)')
    application_id = Column(VARCHAR(32), ForeignKey('application.id', ondelete='CASCADE'), nullable=True,
                            comment='应用ID')
    children = db.relationship('OrgAuthPowerConfig', back_populates='parent', lazy='select', cascade='all, delete-orphan')
    parent = db.relationship('OrgAuthPowerConfig', back_populates='children', remote_side=[id], lazy='select')
    application = db.relationship('Application', backref=backref('org_auth_power_config', cascade='all, delete-orphan'))


# 角色功能表
class OrgRolePower(db.Model):
    __tablename__ = 'org_role_power'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    org_role_id = Column(VARCHAR(32), ForeignKey('org_role_config.id', ondelete='CASCADE'), comment='组织角色ID')
    org_auth_power_config_id = Column(VARCHAR(32), ForeignKey('org_auth_power_config.id', ondelete='CASCADE'),
                                      comment='组织权限的配置表')
    org_auth_power_config = relationship('OrgAuthPowerConfig', backref=backref('org_auth_power_config', cascade = 'all, delete-orphan',
    passive_deletes = True))

    # org_role = relationship('OrgRoleConfig', backref='org_role_power')
    # org_power = relationship('OrgAuthPowerConfig', backref='org_role_power')


# 员工角色表
class OrgStaffRole(db.Model):
    __tablename__ = 'org_staff_role'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    staff_id = Column(VARCHAR(32), ForeignKey('org_staff.id', ondelete='CASCADE'), comment='组织员工ID')
    org_role_config_id = Column(VARCHAR(32), ForeignKey('org_role_config.id', ondelete='CASCADE'), comment='组织的角色ID')

    staff = relationship('OrgStaff', backref=backref('org_staff_role'))
    org_role_config = relationship('OrgRoleConfig', backref=backref('org_staff_role'))
