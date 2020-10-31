from flask import jsonify


class BaseConnector(object):
    type = ''
    url_template = ''
    engine = None
    ds = None

    def __init__(self, ds):
        self.ds = ds

    def connect_url(self):
        raise NotImplementedError()

    def query(self, table_name):
        pass

    def table_names(self):
        if not self.engine:
            return []
        tables = self.engine.table_names()
        res = []
        for table in tables:
            cur = {
                "id": table,
                "name": table
            }
            res.append(cur)
        return res

    def query_with_table(self, table_names):
        sql = 'select * from '
        for name in table_names:
            sql += name + ' inner join '

        if len(sql) > 2:
            index = sql.index('inner')
            sql = sql[0: index]

        try:
            with self.engine.connect() as connection:
                results = connection.execute(sql)
                res = [dict(row) for row in results]

                return res
        finally:
            connection.close()
