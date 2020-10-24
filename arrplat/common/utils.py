import time
import re
import json
import uuid
import decimal
from math import ceil
from random import sample
from extensions import db
from flask import make_response, json
import requests
from arrplat.config import config
import base64
from Crypto.Cipher import AES
from flask import jsonify

def generate_uuid_len(length):
    return str(uuid.uuid4()).replace("-", "")[0:length]


def generate_uuid():
    return str(uuid.uuid4()).replace("-", "")


def generate_random_string(count=5):
    string = "0123456789abcdefghijklmnopqrstuvwxyz"
    return "".join(sample(string, count))


def get_timestamp(is_ms=False):
    current_timestamp = time.time()
    return int(current_timestamp) if not is_ms else int(current_timestamp * 1000)


def get_sql_params(query_sql):
    pattern = r'\$\{(.*?)\}'
    return re.findall(pattern, query_sql)


def valid_email(email):
    return True if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email) else False


def valid_phone(phone):
    phone_rule = "^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\\d{8}$"
    return True if re.match(phone_rule, phone) else False


def valid_phone_code(phone_code):
    return True if len(phone_code) == 6 and phone_code.isdigit() else False


def valid_uuid(input_uuid, has_connect=False):
    if has_connect:
        pattern = r'^\w{8}(-\w{4}){3}-\w{12}'
    else:
        pattern = r'^[\d|a|b|c|d|e|f]{32}'
    return True if re.match(pattern, input_uuid) else False


def valid_url(url):
    pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    return True if re.match(pattern, url) else False


def valid_host(host):
    pattern = r"^http[s]{0,1}://(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
    return True if re.match(pattern, host) else False


def valid_boolean(value):
    return True if value in [0, 1] else False


def valid_not_blank(value):
    return True if value else False


def calculate_page(total_count: int, page: int, page_size: int):
    total_page = ceil(total_count / page_size)
    return {
        "total_page": total_page,
        "page": page,
        "page_size": page_size,
        "total_count": total_count
    }


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


class JsonResponse(object):
    def __init__(self, data, page, message):
        self.data = data
        self.message = message
        self.page = page

        if page:
            self.page = {
                'previous_page': page.previous_page,
                'has_previous': page.has_previous,
                'page': page.page,
                'total': page.total,
                'page_size': page.page_size,
                'next_page': page.next_page,
                'has_next': page.has_next,
            }


def json_response(data: list or dict or None = None, page=None, message=None, status=200):
    status_dict = {
        200: '200 OK',
        401: '401 Unauthorized',
        403: '403 Forbidden',
        404: '404 Not Found',
        409: '409 Resource Exist',
        422: '422 Unprocessable Entity',
        500: '500 Internal Server Error',
    }
    res = jsonify(JsonResponse(data, page, message).__dict__)
    res.status = status_dict[status]
    return res


# TODO 建表前缀问题
# from sqlalchemy.ext.declarative import declared_attr
# import inspect, sys
# class T(db.Model):
#   __abstract__ = True
#   _the_prefix = 'someprefix_'
#
#   @declared_attr
#   def __tablename__(cls):
#     return cls._the_prefix + cls.__incomplete_tablename__

# 执行sql查询语句转为键值对格式
def sql_tuple_to_dict(data: list) -> list:
    if len(data) == 0:
        return data
    keys = list(data[0]._keymap.keys())
    result = []
    for dat in data:
        result.append({key: dat[index] for index, key in enumerate(keys)})
        # 先兼容为null
        # res = {}
        # for index, key in enumerate(keys):
        #     res[key] = dat[index] if dat[index] != None else ""
        # result.append(res)
    return result


# 执行sql获取数据返回
def sql_execute_commit(sql: str):
    res = db.session.execute(sql)
    data = res.fetchall()
    data_list = sql_tuple_to_dict(data)
    db.session.commit()
    return data_list


# 微信解密
class WXBizDataCrypt:
    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        # base64 decode
        sessionKey = base64.b64decode(self.sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))

        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]


# 微信获取用户信息
def wx_get_user_info(code: str, encryptedData: str, iv: str):
    appid = config.get("wx", {}).get("appid", "")
    secret = config.get("wx", {}).get("appsecret", "")
    # 通过code获取用户信息
    res = requests.get(
        f"https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code").json()

    session_key = res["session_key"]
    pc = WXBizDataCrypt(appid, session_key)
    data = pc.decrypt(encryptedData, iv)
    # {'openId': 'okQcr5BeEQN02Etgyhem5gje1RK8', 'nickName': '瘦瘦要变成瘦瘦', 'gender': 1, 'language': 'zh_CN',
    #  'city': 'Chaoyang', 'province': 'Beijing', 'country': 'China',
    #  'avatarUrl': 'https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIXC2byoG7GJKdYVLvEWibbAI9tjcMmy5whWkjgBH52K4wECTdv4Hc4zNKR6MK9NGic5Qia0ICh8Nd0Q/132',
    #  'watermark': {'timestamp': 1583553168, 'appid': 'wx01583ccc3e25c0be'}}

    return data
