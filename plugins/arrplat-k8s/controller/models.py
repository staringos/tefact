
from arrplat.common.utils import generate_uuid, get_timestamp
from extensions import db


class Cluster(db.Model):
    __tablename__ = 'cluster'
    id = db.Column(db.VARCHAR(32), default=generate_uuid, primary_key=True)
    org_id = db.Column(db.ForeignKey('organization.id', ondelete='CASCADE'), comment='组织id')
    user_id = db.Column(db.ForeignKey('user.id'), comment='添加cluster的用户id')
    name = db.Column(db.VARCHAR(64), comment='集群名称')
    host = db.Column(db.VARCHAR(64), comment='集群主机ip')
    port = db.Column(db.SmallInteger(), comment='集群端口(6443..)')
    token = db.Column(db.Text(), comment='远程连接授权的token')
    create_time = db.Column(db.BigInteger(), default=get_timestamp, comment='用户添加集群的时间')
