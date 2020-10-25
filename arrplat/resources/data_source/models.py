import enum
from arrplat.common.base.entity import BaseEntity
from sqlalchemy import Column, VARCHAR, Text, Enum, ForeignKey
from arrplat.common.connector.mysql import MySQLConnector


class DataSourceType(enum.Enum):
    mysql = 'mysql'
    mongodb = 'mongodb'
    postgresql = 'postgresql'
    clickhouse = 'clickhouse'


class DataSourceStatus(enum.Enum):
    connected = 'connected'
    error = 'error'
    lack = 'lack'


class DataSource(BaseEntity):
    __tablename__ = 'ds_data_source'
    name = Column(VARCHAR(32), nullable=False, unique=True, comment='数据源名')
    type = Column(Enum(DataSourceType), comment='数据源类型')
    status = Column(Enum(DataSourceStatus), comment='数据源类型')
    description = Column(Text, comment='数据源描述')

    host = Column(VARCHAR(132), nullable=True, comment='数据源HOST')
    port = Column(VARCHAR(32), nullable=True, comment='端口号')
    username = Column(VARCHAR(132), nullable=True, comment='用户名')
    password = Column(VARCHAR(132), nullable=True, comment='密码')
    default_db = Column(VARCHAR(132), nullable=True, comment='链接默认数据库名称')

    org_id = Column(VARCHAR(32), ForeignKey('organization.id', ondelete='CASCADE'), comment='组织ID')
    create_user_id = Column(VARCHAR(32), ForeignKey('user.id', ondelete='CASCADE'), nullable=False, comment='创建用户ID')

    sql_alchemy_url_template = "mysql+pymysql://{username}:{password}@{host}:{port}/"

    def test(self):
        mysql = MySQLConnector.connect(self)
        mysql.engine.connect()


