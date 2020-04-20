import time
import bcrypt
import base64

from flask_restful import Resource
from marshmallow import fields
from flask_apispec import use_kwargs
from flask_jwt_extended import (
    create_access_token,
    get_current_user
)

from arrplat.common.auth_jwt_utils import user_required
from arrplat.resources.auth.sms_utils import send_phone_code
from arrplat.resources.user.services import UserSchema
from extensions import db
from arrplat.resources.user.models import User, UserInfo, UserPhoneCode
from arrplat.common.get_verify_code import VerifyCodeImg
from arrplat.common.utils import generate_uuid, valid_phone, json_response, valid_phone_code, get_timestamp
from arrplat.common.store_utils import redis_0
from arrplat.config import config

Conf = config.get('system')


class PhoneCodeResource(Resource):
    @use_kwargs({
        "phone": fields.String(required=True, validate=valid_phone),
        "sms_type": fields.String(required=False)
    })
    def post(self, **kwargs):
        """获取手机验证码
          ---
          tags:
            - 登录、注册
          parameters:
            - name: phone
              in: body
              type: string
              required: true
            - name: sms_type
              in: body
              type: string
              required: false
              description: 区分发送端类型
          responses:
            200:
              description: A list of colors (may be filtered by palette)
              examples:
                response: {"data": null, "message": "发送成功"}
        """
        phone = kwargs.get("phone")
        sms_type = kwargs.get("sms_type", "sms")
        user = User.query.filter_by(phone=phone).first()
        user_phone_code = None

        if user:
            user_phone_code = UserPhoneCode.query.filter_by(user_id=user.id).first()
            if user_phone_code and get_timestamp() - user_phone_code.update_time <= 60:
                return json_response(message="验证码请求频繁, 请稍后重试", status=403)
        else:
            user_id = generate_uuid()
            user = User(
                id=user_id,
                phone=phone,
                create_time=get_timestamp(),
                nickname=Conf.get("USER_DISABLE_NICKNAME_PREFIX", 'arrplat_') + phone[-4:]
            )
            user_info = UserInfo(
                user_id=user_id,
                head_url=Conf.get("DEFAULT_HEAD_IMAGE", ""),
                signature="这个人很懒，什么都没留下"
            )
            db.session.add_all([user, user_info])
            db.session.commit()
        # TODO 验证码先用假的的
        payload = send_phone_code(phone)

        if payload["code"] == "OK":
            # 用redis 加失效时间
            redis_0.setex(f"{sms_type}_code_{phone}", 600, payload["phone_code"])
            return json_response(message="获取成功")

        return json_response(message="短信发送失败", status=500)


class VerifyCodeResource(Resource):
    @use_kwargs({
    })
    def get(self):
        """获取图片验证码
          ---
          tags:
            - 登录、注册
          responses:
            200:
              description: A list of colors (may be filtered by palette)
              examples:
                response: {"data": {"verify_code_image": "base64图片", "uuid": "x*32"}, "message": "发送成功"}
        """
        valid_code_object = VerifyCodeImg()
        valid_code_bytes, valid_code_string = valid_code_object.get_verify_code_image()
        valid_code_base64_string = base64.b64encode(valid_code_bytes).decode()
        unique_string = generate_uuid()
        redis_0.set("verify_code:" + unique_string, valid_code_string, ex=Conf.get("VERIFY_CODE_EXPIRE", 180))
        return json_response({
            "verify_code_image": valid_code_base64_string,
            "uuid": unique_string
        })


class PasswordLoginResource(Resource):
    @use_kwargs({
        "phone": fields.String(required=True),
        "password": fields.String(required=True),
        "verify_code": fields.String(required=True),
        "uuid": fields.String(required=True)
    })
    def post(self, **kwargs):
        """密码登录
              ---
          tags:
            - 登录、注册
          parameters:
            - name: phone
              in: body
              type: string
              required: true
            - name: password
              in: body
              type: string
              required: true
            - name: verify_code
              in: body
              type: string
              required: true
            - name: uuid
              in: body
              type: string
              required: true
          responses:
            200:
              description: A list of colors (may be filtered by palette)
              examples:
                response: {"data": {"access_token": "xxx"}, "message": "成功"}
        """
        phone = kwargs.get("phone")
        password = kwargs.get("password")
        verify_code = kwargs.get("verify_code")
        unique_id = kwargs.get("uuid")

        if not valid_phone(phone):
            return json_response(message="无效的手机号", status=403)
        elif len(verify_code) != 4 or not verify_code.isdigit():
            return {"msg": "验证码格式错误"}
        verify_code_redis = redis_0.get("verify_code:" + unique_id)
        if not verify_code_redis:
            return json_response(message="验证码过期，请重新获取", status=403)
        else:
            if verify_code != verify_code_redis.decode():
                return json_response(message="验证码错误", status=403)
            else:
                user = User.query.filter_by(phone=phone).first()
                if not user:
                    return json_response(message="用户不存在", status=404)
                if not user.salt:
                    return json_response(message="您输入的密码有误，请重新输入", status=401)
                password_hashed = bcrypt.hashpw(password.encode(), user.salt.encode())
                if password_hashed != user.password.encode():
                    return json_response(message="您输入的密码有误，请重新输入", status=401)
                access_token = create_access_token(identity=user.id)
                user_schema = UserSchema()
                user_data = user_schema.dump(user).data
                return json_response({
                    "access_token": access_token,
                    "user": user_data,
                }, message="成功")


class PhoneLoginResource(Resource):
    PHONE_VERIFY_CODE_EXPIRE = 600

    @use_kwargs({
        "phone": fields.String(required=True, validate=valid_phone),
        "phone_code": fields.String(required=True, validate=valid_phone_code)
    })
    def post(self, **kwargs):
        """手机验证码登录
          ---
          tags:
            - 登录、注册
          parameters:
            - name: phone
              in: body
              type: string
              required: true
            - name: phone_code
              in: body
              type: string
              required: true
          responses:
            200:
              description: A list of colors (may be filtered by palette)
              examples:
                response: {"data": {"access_token": "jwt 一长串"}, "message": "ok"}
        """
        phone = kwargs.get("phone")
        phone_code = kwargs.get("phone_code")
        # 判断验证码是否过期
        if redis_0.get(f"sms_code_{phone}") and phone_code == str(redis_0.get(f"sms_code_{phone}"), "utf8"):
            user = db.session.query(User).filter(
                User.phone == phone,
            ).first()
        else:
            return json_response(message="验证码错误/过期", status=403)

        access_token = create_access_token(identity=user.id)
        user_schema = UserSchema()
        user_data = user_schema.dump(user).data
        return json_response(data={
            "access_token": access_token,
            "user": user_data,
        }, message="ok")


class PasswordRegisterResource(Resource):
    @use_kwargs({
        'phone': fields.String(required=True),
        'password': fields.String(required=True),
        'again_password': fields.String(required=True),
        'uuid': fields.String(required=True),
        'verify_code': fields.String(required=True)
    })
    def post(self, **kwargs):
        """手机号 密码 注册
          ---
          tags:
            - 登录、注册
          parameters:
            - name: phone
              in: body
              type: string
              required: true
              description: 手机号
            - name: verify_code
              in: body
              type: string
              required: true
              description: 图片验证码
            - name: password
              in: body
              type: string
              required: true
              description: 密码
            - name: again_password
              in: body
              type: string
              required: true
              description: 再次输入密码
            - name: uuid
              in: body
              type: string
              required: true
              description: 验证码的uuid
          responses:
            200:
              description: 成功
              examples:
                response: {"message": "ok"}
            403:
              description: 失败
              examples:
                response: {"message": ["无效的手机号", "验证码格式错误", "两次密码输入不一致", "密码最少需要八位", "验证码过期，请重新获取", "验证码错误"]}
            409:
              description: 手机号已注册
            500:
              description: 注册失败 代码有问题
        """
        phone = kwargs['phone']
        password = kwargs['password']
        again_password = kwargs['again_password']
        verify_code = kwargs['verify_code']
        unique_id = kwargs['uuid']
        password, again_password = password.replace(" ", ""), again_password.replace(" ", "")
        if not valid_phone(phone):
            return json_response(message="无效的手机号", status=403)
        elif len(verify_code) != 4 or not verify_code.isdigit():
            return json_response(message="验证码格式错误", status=403)
        if password != again_password:
            return json_response(message="两次密码输入不一致", status=403)
        if len(password) < 8:
            return json_response(message="密码最少需要八位", status=403)
        verify_code_redis = redis_0.get("verify_code:" + unique_id)
        if not verify_code_redis:
            return json_response(message="验证码过期，请重新获取", status=403)
        else:
            if verify_code != verify_code_redis.decode():
                return json_response(message="验证码错误", status=403)
            else:
                user = User.query.filter_by(phone=phone).first()
                if user:
                    return json_response(message="该手机号已注册", status=409)
                else:
                    try:
                        salt = bcrypt.gensalt()
                        new_password = bcrypt.hashpw(password.encode(), salt)
                        user = User(
                            phone=phone,
                            password=new_password.decode(),
                            salt=salt.decode(),
                            nickname=config['system']['USER_DISABLE_NICKNAME_PREFIX'] + phone[-4:],
                            create_time=time.time()
                        )
                        db.session.add(user)
                        db.session.commit()
                        return json_response(None, message='注册成功', status=200)
                    except Exception as e:
                        _ = e
                        db.session.rollback()
                        return json_response(None, message=f'注册失败{_}', status=500)


class PasswordVerifyResource(Resource):
    @use_kwargs({
        'phone_code': fields.String(required=True, validate=valid_phone_code),
        'phone': fields.String(required=True, validate=valid_phone),
        'password': fields.String(required=True),
        'again_password': fields.String(required=True)
    })
    def post(self, **kwargs):
        """重置密码
          ---
          tags:
            - 登录、注册
          parameters:
            - name: phone
              in: body
              type: string
              required: true
              description: 手机号
            - name: phone_code
              in: body
              type: string
              required: true
              description: 验证码
            - name: password
              in: body
              type: string
              required: true
              description: 密码
            - name: again_password
              in: body
              type: string
              required: true
              description: 再次输入密码
          responses:
            200:
              description: 成功
              examples:
                response: {"message": "ok"}
            403:
              description: 失败
              examples:
                response: {"message": ["验证码错误/过期", "您的密码2次输入有差异", "密码最少需要八位"]}
            409:
              description: 手机号已注册
            500:
              description: 注册失败 代码有问题
        """
        phone_code, phone = kwargs['phone_code'], kwargs['phone']
        password, again_password = kwargs['password'].replace(" ", ""), kwargs['again_password'].replace(" ", "")

        # 判断验证码是否过期
        if redis_0.get(f"sms_code_{phone}") and phone_code == str(redis_0.get(f"sms_code_{phone}"), "utf8"):
            user = db.session.query(User).filter(
                User.phone == phone,
            ).first()
        else:
            return json_response(message="验证码错误/过期", status=403)
        if password != again_password:
            return json_response(message='您的密码2次输入有差异', status=403)
        if len(password) < 8:
            return json_response(message="密码最少需要八位", status=403)

        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(password.encode(), salt)
        try:
            user.salt = salt.decode()
            user.password = password.decode()
            db.session.add(user)
            db.session.commit()
            return json_response(None, message='修改密码成功', status=200)
        except Exception as e:
            _ = e
            db.session.rollback()
            return json_response(None, message='修改密码失败', status=500)

    @user_required
    @use_kwargs({
        'old_password': fields.String(required=True),
        'password': fields.String(required=True),
        'again_password': fields.String(required=True)})
    def put(self, **kwargs):
        """修改密码
          ---
          tags:
            - 登录、注册
          parameters:
            - name: old_password
              in: body
              type: string
              required: true
              description: 老密码
            - name: password
              in: body
              type: string
              required: true
              description: 密码
            - name: again_password
              in: body
              type: string
              required: true
              description: 再次输入密码
          responses:
            200:
              description: 成功
              examples:
                response: {"message": "ok"}
            403:
              description: 失败
              examples:
                response: {"message": ["原密码不正确", "您的密码2次输入有差异", "密码最少需要八位"]}
            409:
              description: 手机号已注册
            500:
              description: 注册失败 代码有问题
        """
        user = get_current_user()

        old_password = kwargs['old_password'].replace(" ", "")
        password = kwargs['password'].replace(" ", "")
        again_password = kwargs['again_password'].replace(" ", "")

        user_password = user.password
        password_hashed = bcrypt.hashpw(old_password.encode(), user.salt.encode()).decode()

        if password != again_password:
            return json_response(message='您的密码2次输入有差异', status=403)
        if len(password) < 8:
            return json_response(message="密码最少需要八位", status=403)
        if user_password != password_hashed:
            return json_response(message='原密码不正确', status=403)

        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(password.encode(), salt)
        try:
            user.salt = salt.decode()
            user.password = password.decode()
            db.session.add(user)
            db.session.commit()
            # TODO 重复代码
            pass
            return json_response(None, message='修改密码成功', status=200)
        except Exception as e:
            _ = e
            db.session.rollback()
            return json_response(None, message='修改密码失败', status=500)
