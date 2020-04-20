from sqlalchemy import Column, \
    ForeignKey, BigInteger, VARCHAR, Text, Enum
from sqlalchemy.dialects.mysql import TINYINT

from arrplat.config import config
from arrplat.common.utils import generate_uuid
from extensions import db
from sqlalchemy.orm import relationship, backref
from arrplat.resources.user.models import User


class Organization(db.Model):
    __tablename__ = 'organization'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    group_type = Column(Enum('GOV', 'Company', 'Personal'), comment='组织类型')
    name = Column(VARCHAR(32), nullable=False, comment='组织名称')
    unique_id = Column(VARCHAR(32), nullable=False, comment='组织唯一ID')
    address = Column(VARCHAR(128), comment='地址')
    website = Column(Text, comment='官网')
    own_user_id = Column(VARCHAR(32), ForeignKey('user.id', ondelete='CASCADE'), comment='拥有人')
    official_company_name = Column(VARCHAR(64), comment='官方公司名称')
    official_org_code = Column(VARCHAR(256), comment='营业执照')
    description = Column(VARCHAR(512), comment='组织描述')
    head_url = Column(Text, default=config['system']['DEFAULT_ORG_HEAD_IMAGE'], comment='组织头像')


class OrgDepartment(db.Model):
    __tablename__ = 'org_department'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    org_id = Column(VARCHAR(32), ForeignKey('organization.id', ondelete='CASCADE'), comment='组织ID')
    name = Column(VARCHAR(32), nullable=False, comment='部门名称')
    parent_id = db.Column(VARCHAR(32), ForeignKey('org_department.id', ondelete='CASCADE'), comment='上级部分')

    organization = relationship('Organization', backref=backref('org_department', cascade='all,delete'), lazy='select')
    child_org_departments = relationship('OrgDepartment', back_populates='parent_org_department')
    parent_org_department = relationship('OrgDepartment', back_populates='child_org_departments', remote_side=[id])


class OrgDepartmentStaff(db.Model):
    __tablename__ = 'org_department_staff'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    org_department_id = Column(VARCHAR(32), ForeignKey('org_department.id', ondelete='CASCADE'), comment='组织部分id')
    staff_id = Column(VARCHAR(32), ForeignKey('org_staff.id', ondelete='CASCADE'), comment='员工id')

    staff = relationship('OrgStaff', backref=backref('org_department_staff', lazy='dynamic', cascade='all,delete'))
    org_department = relationship('OrgDepartment', backref=backref('org_department_staff', lazy='dynamic'))


class OrgStaff(db.Model):
    __tablename__ = 'org_staff'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    user_id = Column(VARCHAR(32), ForeignKey('user.id', ondelete='CASCADE'), comment='用户id')
    org_id = Column(VARCHAR(32), ForeignKey('organization.id', ondelete='CASCADE'), comment='组织id')
    job_title = Column(VARCHAR(32), nullable=False, comment='工作描述')
    is_able = Column(TINYINT, default=1, comment="是否可用(0 false 1 true)")
    superior_id = Column(VARCHAR(32), ForeignKey('org_staff.id', ondelete='CASCADE'), comment='直属上级id')

    organization = relationship('Organization', backref=backref('org_staff', lazy='dynamic'))
    user = relationship(User, backref=backref('org_staff', lazy='dynamic'))
    child_superiors = relationship('OrgStaff', back_populates='parent_superior', lazy='dynamic')
    parent_superior = relationship('OrgStaff', back_populates='child_superiors', remote_side=[id])


class OrgRequest(db.Model):
    __tablename__ = 'org_request'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    create_time = Column(BigInteger, comment='创建时间')
    sender_id = Column(VARCHAR(32), ForeignKey('user.id', ondelete='CASCADE'), comment='发送人用户id')
    receiver_id = Column(VARCHAR(32), ForeignKey('user.id', ondelete='CASCADE'), comment='接收人用户id')
    message = Column(Text)
    org_id = Column(VARCHAR(32), ForeignKey('organization.id', ondelete='CASCADE'), comment='组织id')
    status = Column(TINYINT, default=0, comment='请求状态(0: 已发送 1: 已接受 2: 拒绝)')

    organization = relationship('Organization', backref=backref('org_request', lazy='dynamic'))
    sender = relationship(User, backref=backref('org_request.sender_id', lazy='dynamic'), foreign_keys=sender_id)
    receiver = relationship(User, backref=backref('org_request.receiver_id', lazy='dynamic'),
                            foreign_keys=receiver_id)
