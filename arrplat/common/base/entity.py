from sqlalchemy import Column, BigInteger, VARCHAR
from extensions import db
from arrplat.common.utils import generate_uuid, get_timestamp


"""
basic entity class
"""


class BaseEntity(db.Model):
    __abstract__ = True
    # __table_args__ = {'mysql_charset': 'utf8mb4_bin'}
    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    create_time = Column(BigInteger, default=get_timestamp)
    update_time = Column(BigInteger, default=get_timestamp)
