class BaseConnector(object):
    type = ''
    url_template = ''
    engine = None
    ds = None

    def __init__(self, ds):
        self.ds = ds

    @classmethod
    def connect_url(self):
        raise NotImplementedError()
