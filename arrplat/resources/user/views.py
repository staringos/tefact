from flask_apispec import use_kwargs
from flask_restful import Resource
from marshmallow import fields
from flask_jwt_extended import get_current_user
from sqlalchemy import desc

from arrplat.common.pagination import paginate
from extensions import db
from arrplat.config import config
from arrplat.resources.application.models import Message
from arrplat.resources.application.schema import MessageSchema
from arrplat.resources.organization.models import OrgRequest, Organization, OrgStaff
from arrplat.common.utils import json_response, valid_email, valid_url, valid_uuid, valid_boolean
from arrplat.resources.user.services import UserSchema, UserInfoSchema
from arrplat.resources.user.models import UserInfo, User
from arrplat.common.auth_jwt_utils import user_required

Conf = config.get('qiniu')


class UserInfoResource(Resource):
    @user_required
    def get(self):
        """获取用户基本信息
          ---
          tags:
            - 用户
          responses:
            200:
              description: A list of colors (may be filtered by palette)
              examples:
                response: {"data": {"name": "", "signature": "", "email": ""}, "message": "ok"}
        """
        user = get_current_user()
        user_info = UserInfo.query.filter_by(user_id=user.id).first()

        user_info_schema = UserInfoSchema()
        user_schema = UserSchema()

        response_data = user_info_schema.dump(user_info).data
        response_data.update(user_schema.dump(user).data)

        return json_response(response_data, message="ok")

    @use_kwargs({
        "nickname": fields.String(validate=lambda nickname: True if 2 <= len(nickname.strip()) <= 30 else False),
        "signature": fields.String(),
        "email": fields.String(validate=valid_email),
        "gender": fields.Integer(validate=lambda gender: True if gender in [0, 1] else False),
        "head_url": fields.String(validate=valid_url)
    })
    @user_required
    def put(self, **kwargs):
        """修改用户信息
          ---
          tags:
            - 用户
          parameters:
            - name: nickname
              in: body
              type: string
            - name: signature
              in: body
              type: string
            - name: email
              in: body
              type: string
            - name: gender
              in: body
              type: integer
            - name: head_url
              in: body
              type: integer
          responses:
            200:
              examples:
                response: {"data": null, "message": "修改成功"}
        """
        if not kwargs:
            return json_response(message="参数不能为空", status=422)
        user = get_current_user()
        nickname = kwargs.get("nickname")
        if nickname:
            user.nickname = nickname
            db.session.add(user)
        user_info = UserInfo.query.filter_by(user_id=user.id).first()
        if user_info:
            for key, value in kwargs.items():
                setattr(user_info, key, value)
        else:
            user_info = UserInfo(**kwargs, user_id=user.id)
        db.session.add(user_info)
        db.session.commit()
        return json_response(message="修改成功")


class UserInviteesMessage(Resource):
    @use_kwargs({
    })
    def get(self, org_request_id):
        """登录界面的邀请提示
          ---
          tags:
            - 用户
          parameters:
            - name: org_request_id
              in: url
              type: string
              required: true
              description: 组织邀请id
          responses:
            200:
              examples:
                response: {"data": {"org_request_message": "158282382ad547fc920c54c44dbd015f"}, "message": "ok"}
        """
        query_result = db.session.query(User.nickname, Organization.name) \
            .join(OrgRequest, OrgRequest.org_id == Organization.id) \
            .filter(OrgRequest.sender_id == User.id, OrgRequest.id == org_request_id).first()

        if not query_result:
            return json_response(message="没有找到邀请信息", status=404)

        org_request_message = "用户 %s 邀请您加入 %s" % (query_result.nickname, query_result.name)
        data = {
            "org_request_message": org_request_message
        }
        return json_response(data=data, message="ok")


class UserMessageDetailResource(Resource):
    @user_required
    def put(self, message_id):
        """修改状态
          ---
          tags:
            - 用户
          parameters:
            - name: has_detail
              in: path
              type: string
              required: True
              description: 消息id
          responses:
            200:
              examples:
                response: {"data": null, "message": "设置已读成功"}
            404:
              examples:
                response: {"data": null, "message": "找不到对应的消息"}
            500:
              examples:
                response: {"data": null, "message": "设置已读失败"}
        """
        user = get_current_user()
        message_query = db.session.query(Message) \
            .filter(Message.id == message_id, Message.user_id == User.id, User.id == user.id)

        message = message_query.first()
        if not message:
            return json_response(message="找不到对应的消息", status=404)
        try:
            message_query.update({Message.is_read: 1}, synchronize_session=False)
            db.session.commit()
        except Exception as e:
            _ = e
            return json_response(message="设置已读失败", status=500)
        else:
            return json_response(message="设置已读成功")


class UserMessageResource(Resource):
    @use_kwargs({
        "has_detail": fields.Integer(validate=valid_boolean),
        "org_id": fields.String(validate=valid_uuid),
        "page": fields.Integer(),
        "page_size": fields.Integer()
    }, locations=['querystring'])
    @user_required
    def get(self, **kwargs):
        """获取消息
          ---
          tags:
            - 用户
          parameters:
            - name: has_detail
              in: querystring
              type: int
              required: false
              description: 是否需要详细，如果为0返回未读的消息数量 0|1
            - name: org_id
              in: querystring
              type: string
              required: false
              description: 组织id，如果存在，表示获取该组织下的用户消息，否则表示全部
            - name: page
              in: querystring
              type: int
              required: false
              description: 当前页
            - name: page_size
              in: querystring
              type: int
              required: false
              description: 一页的消息数量
          responses:
            200:
              examples:
                response: {
                  "data":{
                    "message_list": [
                      {
                        "id": "c77e641fbe9d472398feb89666087eee",
                        "is_read": 1,
                        "title": "xxx",
                        "content": "xxx",
                        "send_time": 1577328935,
                        "read_time": read_time,
                        "message_type": "消息类型(1. system系统 2. plus插件 3. org组织 4. invitee邀请"
                      }
                    ]
                  },"message": "ok"}
        """
        user = get_current_user()
        org_id = kwargs.get("org_id")
        has_detail = kwargs.get("has_detail")
        page = kwargs.get("page", 1)
        page_size = kwargs.get("page_size", 10)

        base_query = db.session.query(Message) \
            .filter(Message.user_id == User.id, User.id == user.id)
        if org_id:
            base_query = base_query.filter(Message.organization_id == org_id)
        unread_count = base_query.filter(Message.is_read == 0).count()
        if not has_detail:
            return json_response(data={"unread_count": unread_count}, message="ok")

        if org_id:
            base_query = base_query.fitler(Message.organization_id == org_id)

        message_query = base_query.order_by(Message.is_read.asc(), desc(Message.send_time))
        message_paginate = paginate(message_query, page, page_size)
        try:
            pass
        except Exception as e:
            _ = e
            return json_response(message="消息数据获取失败", status=500)
        else:
            message_schema = MessageSchema(many=True, only=(
                            "id", "is_read", "title", "content", "send_time", "read_time", 'message_type'))
            data = {
                "message_list": message_schema.dump(message_paginate.items).data,
                "unread_count": unread_count
            }
            return json_response(data=data, message="ok", page=message_paginate)


class UserOrganizationResource(Resource):
    @user_required
    def delete(self, org_id):
        """退出组织
          ---
          tags:
            - 用户
          parameters:
            - name: org_id
              in: path
              type: int
              required: True
              description: 要退出的组织id
          responses:
            200:
              examples:
                response: {"data": null, "message": "退出组织成功"}
            403:
              examples:
                response: {"data": null, "message": "您是组织创建人，无法直接退出组织"}
            404:
              examples:
                response: {"data": null, "message": "您未加入该组织"}
        """
        user = get_current_user()
        query_result = db.session.query(OrgStaff.id, OrgStaff.job_title).filter(
            OrgStaff.org_id == org_id, OrgStaff.user_id == user.id).first()
        if not query_result:
            return json_response(message="您未加入该组织", status=404)
        if query_result.job_title == "组织创建人":
            return json_response(message="您是组织创建人，无法直接退出组织", status=403)
        db.session.query(OrgStaff).filter(OrgStaff.id == query_result.id).delete()
        db.session.commit()
        return json_response(message="退出组织成功")
