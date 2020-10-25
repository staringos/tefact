class BaseConnector(object):
    type = ''
    url_template = ''
    engine = None
    ds = None

    def __init__(self, ds):
        self.ds = ds

    def connect_url(self):
        raise NotImplementedError()

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
