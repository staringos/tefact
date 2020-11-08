from flask_restful import Resource
from flask_apispec import use_kwargs
from extensions import db
from .models import SharePage, ShareType
from .schema import SharePageSchema
from arrplat.resources.page.services import allow_access_page
from arrplat.common.auth_jwt_utils import user_required
from arrplat.common.get_verify_code import VerifyCodeImg
from marshmallow import fields
from flask_jwt_extended import get_current_user
from arrplat.common.utils import json_response, generate_uuid_len


class AddShareResource(Resource):
    @user_required
    @use_kwargs({
        'type': fields.String(required=True),
    })
    def post(self, page_id, **kwargs):
        """页面分享
           ---
           tags:
             - 分享
           parameters:
           responses:
             200:
               examples:
                 response: {"data": null, "message": "添加成功"}
         """
        user = get_current_user()
        page, org_id = allow_access_page(page_id, user.id)

        if not page or page.__class__.__name__ != "Page":
            return page

        share = db.session.query(SharePage).filter(SharePage.page_id == page_id).first()
        key = generate_uuid_len(6)
        password = generate_uuid_len(6)

        if not share:
            share = SharePage(
                page_id=page.id,
                key=key,
                password=password,
                type=kwargs.get("type"),
                create_user_id=user.id,
                org_id=org_id
            )
        else:
            share.type = kwargs.get("type")

        if type == ShareType.password:
            share.password = VerifyCodeImg.get_random_str()

        db.session.add(share)
        db.session.commit()

        return json_response(message="分享成功", data={
            "id": share.id,
            "key": share.key,
            "password": share.password
        })


class SharePageResource(Resource):
    share_page_schema = SharePageSchema()

    @use_kwargs
    def get(self, share_key):
        """查询分享页面基本信息
           ---
           tags:
             - 分享
           parameters:
           responses:
             200:
               examples:
                 response: {"data": null, "message": "添加成功"}
         """
        page = db.session.query(SharePage).filter(SharePage.key == share_key).first()

        if not page:
            return json_response(message="页面未找到", status=404)

        try:
            data = self.share_page_schema.dump(page).data
            return json_response(data=data, status=200)
        except Exception as e:
            return json_response(message=str(e), status=409)

