import enum
from sqlalchemy import Column, Integer, \
    ForeignKey, Enum, BigInteger, VARCHAR, Text
from sqlalchemy.dialects.mysql import TINYINT
from arrplat.common.base.entity import BaseEntity
from arrplat.common.utils import generate_uuid, get_timestamp


class ShareType(enum.Enum):
    free = 'free'
    password = 'password'
    login = 'login'
    within_org = 'within_org'


class SharePage(BaseEntity):
    type_enum = {
        0: 'default',
        1: 'third',
        2: 'light',
    }
    __tablename__ = 'share_page'
    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    key = Column(VARCHAR(32), nullable=False, unique=True, comment='公开的页面KEY')
    type = Column(Enum(ShareType), comment='数据源类型')
    head_image = Column(Text, comment='微信等应用分享头图')

    page_id = Column(VARCHAR(32), ForeignKey('page.id', ondelete='CASCADE'), comment='分享页面ID')
    password = Column(VARCHAR(32))

    unique_id = Column(VARCHAR(32), default=generate_uuid)
    org_id = Column(VARCHAR(32), ForeignKey('organization.id', ondelete='CASCADE'), comment='组织ID')
    create_user_id = Column(VARCHAR(32), ForeignKey('user.id', ondelete='CASCADE'), nullable=False, comment='分享发起用户ID')
