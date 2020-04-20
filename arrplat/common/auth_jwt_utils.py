from flask import jsonify, Blueprint
from arrplat.common.store_utils import redis_0
from arrplat.common.utils import json_response
from arrplat.resources.auth.models import OrgStaffRole, OrgRolePower, OrgAuthPowerConfig, OrgRoleConfig
from arrplat.resources.organization.models import OrgStaff

from arrplat.resources.user.models import User
from extensions import jwt, db
from flask_jwt_extended import verify_jwt_in_request, verify_jwt_in_request_optional, get_jwt_identity, \
    jwt_refresh_token_required, create_access_token, decode_token
from functools import wraps

blueprint = Blueprint('login', __name__, url_prefix='/auth')


@blueprint.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    res = {
        'access_token': create_access_token(identity=current_user)
    }

    return jsonify(res), 200


"""
2019-12-11

  这里使用了user_loader_callback_loader装饰器来添加一个回调函数，用来获取id=identity的用户，存储到了_app_ctx_stack.top.jwt_user中，
      （from flask import _app_ctx_stack    --->   _app_ctx_stack.top.jwt_user）
而后续user_required函数里面还是有获取了一次user，这里的jwt_user也没有使用到，所以可以先注释掉这里。
"""


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    return User.query.get(identity)


def add_old_token_to_blacklist(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        if isinstance(result, dict) and result.get("access_token") is not None:
            access_token = result["access_token"]
            res = decode_token(access_token)
            if res:
                identity = res["identity"]
                access_jti = res["jti"]
                redis_0.set("soco:access_token:{}".format(identity), access_jti)
        return result

    return wrapper


def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            _ = e
            return json_response(None, message='not found token', status=401)
        # 这里没必要去获取user，因为只有去判断用户是否存在，只需要id就够了
        # user = User.query.filter_by(id=get_jwt_identity(), is_able=1).first()
        user_id = db.session.query(User.id).filter(User.id == get_jwt_identity(), User.is_able == 1).first()
        db.session.commit()
        if not user_id:
            return json_response(None, status=401)

        return add_old_token_to_blacklist(fn)(*args, **kwargs)

    return wrapper


def user_verify_optional(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request_optional()
        if get_jwt_identity():
            user = User.query.filter_by(id=get_jwt_identity(), is_able=1).first()
            if not user:
                return {"msg": "无权限访问"}, 403
        return add_old_token_to_blacklist(fn)(*args, **kwargs)

    return wrapper


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    identity = decrypted_token['identity']
    jti = decrypted_token['jti']
    entry = redis_0.get("soco:access_token:{}".format(identity))
    if entry is None:
        return True
    return entry != jti.encode()


def platform_role_required(url_name=''):
    def wrapper(func):
        def f(*args, **kwargs):
            org_id = kwargs.get('id')
            if not org_id:
                return json_response(None, message='没有组织ID信息', status=200)
            org_obj = OrgStaff.query.join(User).filter(User.id == get_jwt_identity(), User.is_able == 1,
                                                       OrgStaff.org_id == org_id).first()
            if not org_obj:
                return json_response(None, message='没有用户信息或者该用户已被禁用', status=401)
            ret = func(*args, **kwargs)
            role_obj = db.session.query(OrgStaff).filter(OrgStaff.id == org_obj.id).join(OrgStaffRole, OrgRoleConfig,
                                                                                         OrgRolePower,
                                                                                         OrgAuthPowerConfig).filter(
                OrgAuthPowerConfig.name == url_name).all()
            if not role_obj:
                return json_response(None, message='该用户没有角色权限访问', status=401)

            return ret

        return f

    return wrapper
