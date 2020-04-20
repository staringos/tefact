from redis import StrictRedis
from arrplat.config import config


class DBUtils(object):
    # redis
    @staticmethod
    def get_redis_client(redis_config):
        return StrictRedis(redis_config['host'], redis_config['port'], redis_config['db'], redis_config['password'])


redis_0 = DBUtils.get_redis_client(config.get('redis'))

