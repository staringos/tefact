import os
import datetime
import json

basedir = os.path.abspath(os.path.dirname(__file__))

f = open("arrplat.config.json", encoding='utf-8')
setting = json.load(f)

db = {
    'host': '60.205.155.215',
    'user': 'tefact',
    'passwd': 'M4RjfPn6SjSGBXYN',
    'port': 3306,
    'db': 'tefact'
}
# db = {
#     'host': 'rm-2zee2288spst1957llo.mysql.rds.aliyuncs.com',
#     'user': 'root',
#     'passwd': 'QUiiNdhqRX1Nmw6C',
#     'port': 3306,
#     'db': 'arrplat_py_test'
# }

database_uri = os.environ.get('DEV_DATABASE_URL') or \
               "mysql+pymysql://{}:{}@{}:{}/{}".format(db['user'], db['passwd'], db['host'],
                                                       db['port'], db['db'])

config = {
    'product': {
        'name': 'Arrplat',
        'description': 'PaaS framework',
    },
    'db': db,
    'redis': {
        'host': '182.92.86.109',
        'password': 'ciwq7QjAPWR6UciE',
        'port': 6379,
        'db': 0
    },
    'qiniu': {
        'domain': 'soco.cdn.arrway.cn',
        'access_key': 'gMTIlS1akA2QbQhrpCNS9tfSsFqMRru2ExLYtVfY',
        'secret_key': 'xxm8yO1Nit8LnU25KES78XVP569fnvVM0PWQyYQf',
        'bucket_name': 'soco',
        'info': {
            'soco': ('soco', 'soco.cdn.arrway.cn', ('png', 'jpg', 'jpeg', 'gif', 'ico')),
            'arrplat': ('arrplat', 'arrplatimg.arrway.cn', ('png', 'jpg', 'jpeg', 'gif', 'ico')),
        }
    },
    'message': {
        'ACCESS_KEY_ID': 'LTAI4FvB51TN4prpe68kadrX',
        'ACCESS_KEY_SECRET': 'RV1Tde9qvCLxm1KmSlBnpjmQx1ugjt',
        'REGION': 'cn-hangzhou',
        'PRODUCT_NAME': 'Dysmsapi',
        'DOMAIN': 'dysmsapi.aliyuncs.com'
    },

    'setting': setting,

    'system': {
        'SQLALCHEMY_DATABASE_URI': database_uri,
        'USER_DISABLE_NICKNAME_PREFIX': 'arrplat_',
        'LOG_FILE_PATH': '~/errors/soco-api-errors.log',
        'FONT_PATH': os.path.join(basedir, 'common/font.ttf'),
        'DEFAULT_HEAD_IMAGE': 'http://springimg.arrway.cn/c98d3b06b1584d13af38252c37454a75.png',
        'DEFAULT_ORG_HEAD_IMAGE': 'https://soco.cdn.arrway.cn/orgHeadImage.png',
        'VERIFY_CODE_EXPIRE': 180,
        'BASEDIR': basedir,
        'SECRET_KEY': os.environ.get('SECRET_KEY') or 'pay-IKJNDFB',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_RECORD_QUERIES': True,
        'ACCESS_EXPIRES': datetime.timedelta(days=7),
        'REFRESH_EXPIRES': datetime.timedelta(days=30),
        'JWT_ACCESS_TOKEN_EXPIRES': False,
        'JWT_REFRESH_TOKEN_EXPIRES': False,
        # 'JWT_BLACKLIST_ENABLED': True,
        'JWT_BLACKLIST_TOKEN_CHECKS': ['access', 'refresh']
    },
    'wx': {
        "appid": "wx01583ccc3e25c0be",
        "appsecret": "409eefa382b8bf041589162efe805cea"
    }

}
redis_key = {
    "user_select_history": "user_select_history"

}
DEBUG = True
DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 15
