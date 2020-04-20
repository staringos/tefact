from sqlalchemy import Column, Integer, \
    ForeignKey, BigInteger, CHAR, VARCHAR

from arrplat.common.utils import generate_uuid
from extensions import db


class Tag(db.Model):
    __tablename__ = 'book_tag'
    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    origin_link = Column(VARCHAR(128), comment='原始链接')
    name = Column(VARCHAR(20), nullable=True, comment='标签名')


class Book(db.Model):
    __tablename__ = 'book_book'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    origin_id = Column(VARCHAR(128), comment='原始ID')
    name = Column(VARCHAR(20), nullable=True, comment='书名')
    description = Column(VARCHAR(128), comment='描述')
    star = Column(VARCHAR(128), comment='评分')
    author = Column(VARCHAR(128), comment='作者')
    translator = Column(VARCHAR(128), comment='译者')
    press_name = Column(VARCHAR(128), comment='出版社')
    head_image = Column(VARCHAR(128), comment='封面')
    star = Column(VARCHAR(128), comment='评分')
    comment_num = Column(VARCHAR(128), comment='评论数')
    link = Column(VARCHAR(128), comment='原始链接')
    create_time = Column(BigInteger, comment='注册时间')
    publish = Column(BigInteger, comment='出版时间')

    def __repr__(self):
        return '<{}: phone: {} >'.format(
            self.__class__.__name__, self.name
        )

    __str__ = __repr__
