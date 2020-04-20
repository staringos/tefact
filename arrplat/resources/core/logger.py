import logging
from arrplat.config import config
import os
from functools import partial

API_CONFIG = os.environ.get('API_CONFIG', 'development')
Conf = config.get('system')


class EnvLogger:
    """
        example:
           env_logger = EnvLogger(__name__).env_getlogger()
           env_logger.info('foo')
    """
    def __init__(self, env_name, mod_name):
        self.env_name = env_name
        self.mod_name = mod_name

    @staticmethod
    def _getlogger(mod_name: str, file_path: str = "", log_level=logging.INFO,
                   handler_level=logging.INFO, is_print=True):
        logger = logging.getLogger(mod_name)
        logger.setLevel(log_level)
        logger.propagate = False
        if is_print:
            handler = logging.StreamHandler()
        else:
            if file_path:
                handler = logging.FileHandler(file_path)
            else:
                raise ValueError("file_path not empty ")
        handler.setLevel(handler_level)
        formatter = logging.Formatter(fmt="%(asctime)s [%(name)s %(funcName)s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def env_getlogger(self):
        if self.env_name == "development":
            return self._getlogger(self.mod_name)
        if self.env_name == "production":
            return self._getlogger(self.mod_name, is_print=False, file_path=Conf.get('LOG_FILE_PATH'))


EnvLogger = partial(EnvLogger, API_CONFIG)
