from sqlalchemy import Column, \
    ForeignKey, JSON, VARCHAR, Enum
from arrplat.common.utils import generate_uuid
from arrplat.common.base.entity import BaseEntity
import enum


class FormType(enum.Enum):
    default = 'default'


class Form(BaseEntity):
    __tablename__ = 'form'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    title = Column(VARCHAR(32))
    description = Column(VARCHAR(512), comment='表单描述')
    type = Column(Enum(FormType), comment='数据源类型')

    config = Column(JSON, comment='表单元素配置')

    unique_id = Column(VARCHAR(32), default=generate_uuid)
    create_user_id = Column(VARCHAR(32), ForeignKey('user.id', ondelete='CASCADE'), comment='拥有人')
    org_id = Column(VARCHAR(32), ForeignKey('organization.id', ondelete='CASCADE'), comment='组织ID')


class FormData(BaseEntity):
    __tablename__ = 'form_data'
    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    data = Column(JSON, comment='表单元素配置')
    submitter_info = Column(JSON, comment='提交者信息')

    create_user_id = Column(VARCHAR(32), ForeignKey('user.id', ondelete='CASCADE'), comment='拥有人')
    form_id = Column(VARCHAR(32), ForeignKey('form.id', ondelete='CASCADE'), comment='表单ID')
