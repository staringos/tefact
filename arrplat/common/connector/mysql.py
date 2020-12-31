from .base import BaseConnector
from sqlalchemy.engine.url import make_url
from sqlalchemy import create_engine


class MySQLConnector(BaseConnector):
    url_template = "mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    ds = None

    def __init__(self, ds):
        self.ds = ds

    def connect_url(self):
        ds = self.ds
        return make_url(
            self.url_template.format(
                username=ds.username, password=ds.password, host=ds.host, port=ds.port, database=ds.default_db
            )
        )

    @staticmethod
    def connect(ds):
        mysql = MySQLConnector(
            ds=ds
        )

        mysql.engine = create_engine(mysql.connect_url())
        mysql.engine.connect()
        return mysql
