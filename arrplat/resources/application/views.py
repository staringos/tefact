from marshmallow import fields, Schema
from flask_apispec import use_kwargs
from extensions import db
from arrplat.resources.organization.models import Organization
from .models import OrgApplication

from flask_restful import Resource
from .models import Application, ApplicationMenus
from arrplat.common.utils import json_response, generate_uuid_len, valid_uuid, valid_phone, valid_boolean
from arrplat.resources.application.schema import ApplicationSchema
from arrplat.resources.page.models import Page
from arrplat.resources.page.schema import PageSchema


class LightAppModifyResource(Resource):
    platform = 'pc'
    app_schema = ApplicationSchema(many=False, platform=platform)
    page_schema = PageSchema(many=True)

    def get(self, id):
        """获取轻应用详情
          ---
          tags:
            - 轻应用
          parameters:
            - name: id
              in: body
              type: string
              required: true
        """
        app = db.session.query(Application) \
            .filter(Application.id == id).first()

        if not app:
            return json_response(message="找不到应用", status=404)

        res = self.app_schema.dump(app).data
        pages = db.session.query(Page).filter(Page.application_id == id).all()

        res['pages'] = self.page_schema.dump(pages).data

        return json_response(res)

    @use_kwargs({
    })
    def delete(self, id):
        """创建轻应用
          ---
          tags:
            - 轻应用
          parameters:
            - name: title
              in: body
              type: string
              required: true
        """
        app = db.session.query(Application) \
            .filter(Application.id == id).first()

        if not app:
            return json_response(message="找不到应用", status=404)

        if not app.type == 2:
            return json_response(message="不能删除非轻应用", status=403)

        db.session.delete(app)
        db.session.commit()
        return json_response(message="删除成功")


class LightAppResource(Resource):
    @use_kwargs({
        "title": fields.String(required=True),
        "org_id": fields.String(required=True),
        "description": fields.String(required=False)
    })
    def post(self, **kwargs):
        """创建轻应用
          ---
          tags:
            - 应用
          parameters:
            - name: title
              in: body
              type: string
              required: true
            - name: org_id
              in: body
              type: string
              required: true
            - name: description
              in: body
              type: string
              required: false
          responses:
            200:
              description: A list of colors (may be filtered by palette)
              examples:
                response: {"data": null, "message": "添加成功"}
        """
        org = db.session.query(Organization).filter(Organization.id == kwargs.get("org_id")).first()
        if not org:
            return json_response(message=f"组织ID错误", status=403)

        app_name = generate_uuid_len(7)

        app = Application(
            name=app_name,
            admin_route=app_name,
            api_route=app_name,
            title=kwargs.get("title"),
            description=kwargs.get("description"),
            icon="/app.png",
            is_official=False,
            own_org_id=org.id,
            type=2,
            visible=1
        )
        db.session.add(app)
        db.session.commit()

        index_menu = ApplicationMenus(
            application_id=app.id,
            name="首页",
            icon="",
            link="/light/" + app.admin_route,
            platform="pc,mobile",
            sort=1
        )

        org_app = OrgApplication(
            organization_id=org.id,
            application_id=app.id,
            status=1
        )

        db.session.add(index_menu)
        db.session.add(org_app)
        db.session.commit()

        return json_response(message="添加成功", data={
            "id": app.id
        })


class LightAppPage(Resource):
    @use_kwargs({
        "title": fields.String(required=True),
        "app_id": fields.String(required=True),
        "direction": fields.String(required=False),
    })
    def post(self, **kwargs):
        """添加应用页面
          ---
          tags:
            - 轻应用
          parameters:
            - name: id
              in: body
              type: string
              required: true
        """
        app_id = kwargs.get('app_id')
        app = db.session.query(Application).filter(Application.id == app_id).first()

        if not app:
            return json_response(message="找不到应用", status=404)

        direction = kwargs.get('direction')
        key = generate_uuid_len(7)

        page = Page(
            key=key,
            title=kwargs.get('title'),
            application_id=app.id,
            direction=Page.string_to_direction_type(direction),
        )

        db.session.add(page)
        db.session.commit()

        return json_response(message="添加成功", data={
            "id": page.id
        })


class LightAppMenu(Resource):
    @use_kwargs({
        "app_id": fields.String(required=True),
        "name": fields.String(required=True),
        "application_id": fields.String(required=True),
        "icon": fields.String(required=False),
        "link": fields.String(required=False),
        "type": fields.String(required=True),
        "page_key": fields.String(required=False),
        "parent_id": fields.String(required=False),
        "page_id": fields.String(required=False),
    })
    def post(self, **kwargs):
        app_id = kwargs.get('app_id')
        app = db.session.query(Application).filter(Application.id == app_id).first()

        if not app:
            return json_response(message="找不到应用", status=404)

        """添加应用菜单
          ---
          tags:
            - 轻应用
          parameters:
            - name: id
              in: body
              type: string
              required: true
        """
        menu = ApplicationMenus(
            name=kwargs.get('name'),
            application_id=kwargs.get('application_id'),
            icon=kwargs.get('icon'),
            link=kwargs.get('link'),
            type=ApplicationMenus.page_type_enum[kwargs.get('type')],
            page_key=kwargs.get('page_key'),
            platform=kwargs.get('platform'),
            sort=kwargs.get('sort'),
            parent_id=kwargs.get('parent_id'),
            page_id=kwargs.get('page_id'),
        )
        db.session.add(menu)
        db.session.commit()

        return json_response(message="添加成功", data={
            "id": menu.id
        })
