from extensions import db
from sqlalchemy import Column, Enum, \
    ForeignKey, DateTime, BigInteger, VARCHAR, Text
from arrplat.common.utils import generate_uuid, get_timestamp
import enum


class DataSourceType(enum.Enum):
    mysql = 1
    csv = 2
    excel = 3


class SupportDB(enum.Enum):
    mysql = 1


class DataTableType(enum.Enum):
    table = 1
    view = 2
    custom = 3


class FieldType(enum.Enum):
    origin = 1
    custom = 2


class FieldDataType(enum.Enum):
    string = 1
    number = 2
    date = 3


class DataSource(db.Model):
    __tablename__ = 'ds_data_source'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    name = Column(VARCHAR(32), nullable=False, unique=True, comment='官方唯一的名')
    type = Column(Enum(DataSourceType), comment='数据源类型')
    file_path = Column(VARCHAR(300), comment='文件数据源的存储位置')
    desc = Column(VARCHAR(50))


class DataBaseConnector(db.Model):
    __tablename__ = 'ds_data_base_connect'
    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    data_source_id = Column(VARCHAR(32), ForeignKey('datasource.id', ondelete="CASCADE"), comment='数据源ID')
    db_name = Column(Enum(SupportDB), comment='链接默认数据库')
    host = Column(VARCHAR(50))
    port = Column(VARCHAR(50))
    username = Column(VARCHAR(50))
    password = Column(VARCHAR(50))
    url = Column(VARCHAR(500))
    db_name = Column(VARCHAR(500))


class DataBase(db.Model):
    __tablename__ = 'ds_data_base'
    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    data_source_id = Column(VARCHAR(32), ForeignKey('datasource.id', ondelete="CASCADE"), comment='数据源ID')
    db_name = Column(Enum(SupportDB), comment='数据源类型')


class DataTable(db.Model):
    __tablename__ = 'ds_data_table'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    data_source_id = Column(VARCHAR(32), ForeignKey('datasource.id', ondelete="CASCADE"), comment='数据源ID')
    name = Column(VARCHAR(50))
    type = Column(Enum(DataTableType))


class DataFields(db.Model):
    __tablename__ = 'ds_data_field'

    id = Column(VARCHAR(32), default=generate_uuid, primary_key=True)
    data_source_id = Column(VARCHAR(32), ForeignKey('datasource.id', ondelete="CASCADE"), comment='数据源ID')
    name = Column(VARCHAR(50))
    type = Column(Enum(FieldType))
