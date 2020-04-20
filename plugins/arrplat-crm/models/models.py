from sqlalchemy import Column, Integer, \
    ForeignKey, BigInteger, CHAR, VARCHAR, Text
from sqlalchemy.dialects.mysql import TINYINT

from arrplat.common.utils import generate_uuid
from arrplat.config import config
from extensions import db
from sqlalchemy.orm import relationship, backref


class Customer(db.Model):
    __tablename__ = 'crm_customer'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(20), nullable=True)
    description = Column(VARCHAR(128))
    create_time = Column(BigInteger, comment='注册时间')

    def __repr__(self):
        return '<{}: phone: {} >'.format(
            self.__class__.__name__, self.name
        )

    __str__ = __repr__
