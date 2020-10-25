from .base import BaseConnector
from sqlalchemy.engine.url import make_url
from sqlalchemy import create_engine


class MySQLConnector(object):
    url_template = "mysql+pymysql://{username}:{password}@{host}:{port}/"
    ds = None

    def __init__(self, ds):
        self.ds = ds
        print("self")
        print(self)
        print(self.ds)

    def connect_url(self):
        ds = self.ds
        return make_url(
            self.url_template.format(
                username=ds.username, password=ds.password, host=ds.host, port=ds.port
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
