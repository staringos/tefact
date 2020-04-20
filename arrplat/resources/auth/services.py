from arrplat.common.store_utils import redis_0
from flask_jwt_extended import get_jti


def add_access_token_to_redis(user_id, access_token):
    access_jti = get_jti(encoded_token=access_token)
    redis_0.set("soco:access_token:{}".format(user_id), access_jti)
