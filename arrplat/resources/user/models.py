from sqlalchemy import Column, Integer, \
    ForeignKey, BigInteger, CHAR, VARCHAR, Text
from sqlalchemy.dialects.mysql import TINYINT

from arrplat.common.utils import generate_uuid
from arrplat.config import config
from extensions import db
from sqlalchemy.orm import relationship, backref


class User(db.Model):
    __tablename__ = 'user'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    phone = Column(VARCHAR(20), nullable=True)
    password = Column(VARCHAR(128))
    salt = Column(VARCHAR(32), comment="密码加盐")
    nickname = Column(VARCHAR(30))
    name = Column(VARCHAR(30))
    is_able = Column(TINYINT, default=1, comment='是否启用 0:false  1:true')
    create_time = Column(BigInteger, comment='注册时间')
    is_invite_status = Column(TINYINT, default=0, comment='是否是被邀请的用户。0: 非邀请用户，1: 被邀请，但是没有登陆, 2: 被邀请，已经同意登陆过')
    last_login_time = Column(BigInteger, comment='最后登陆时间')

    def __repr__(self):
        return '<{}: phone: {} >'.format(
            self.__class__.__name__, self.phone
        )

    __str__ = __repr__


class UserInfo(db.Model):
    __tablename__ = 'user_info'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    gender = Column(TINYINT)  # 0 female 1 male
    head_url = Column(Text, default=config['system']['DEFAULT_HEAD_IMAGE'], comment="头像")
    signature = Column(Text, comment="个性签名", default="这个人很懒，什么都没留下")
    email = Column(VARCHAR(128))
    user_id = Column(VARCHAR(32), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', backref=backref('user_info', uselist=False), uselist=False)

    def __repr__(self):
        return '<{}: user_id: {} id: {}>'.format(
            self.__class__.__name__, self.user_id, self.id
        )

    __str__ = __repr__


class UserPhoneCode(db.Model):
    __tablename__ = 'user_phone_code'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    user_id = Column(VARCHAR(32), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    code = Column(CHAR(6))
    create_time = Column(BigInteger)
    update_time = Column(BigInteger)
    valid_time = Column(Integer)
    position = Column(VARCHAR(30))
