from marshmallow import fields, Schema
from flask_apispec import use_kwargs
from extensions import db
from arrplat.resources.organization.models import Organization
from .models import OrgApplication

from flask_restful import Resource
from .models import Application, ApplicationMenus
from arrplat.common.utils import json_response, generate_uuid_len, valid_uuid, valid_phone, valid_boolean
from arrplat.resources.application.schema import ApplicationSchema
from arrplat.resources.page.models import Page, PageSection
from arrplat.resources.page.schema import PageSchema, PageSectionSchema
import time


class PageSectionResource(Resource):
    def delete(self, page_id, section_id):
        section = db.session.query(Page).filter(Page.id == section_id).first()
        if not section:
            return json_response(message="找不到页面", status=404)

        db.session.delete(section)
        db.session.commit()
        return json_response("删除成功!")


class PageSectionListResource(Resource):
    page_section_schema = PageSectionSchema(many=False)

    @use_kwargs({
        "title": fields.String(required=False),
        "section_type": fields.String(required=True),
        "nodes": fields.List(fields.Dict, required=False)
    })
    def post(self, page_id, **kwargs):
        section = PageSection(
            section_type=PageSection.string_to_data_type(kwargs.get('section_type')),
            page_id=page_id,
            nodes=kwargs.get('nodes', []),
            create_time=time.time()
        )

        db.session.add(section)
        db.session.commit()

        data = self.page_section_schema.dump(section).data

        return json_response(data=data, message="添加成功")


class LightPageResource(Resource):
    page_schema = PageSchema(many=False)

    @use_kwargs({
        "title": fields.String(required=False),
        "type": fields.String(required=False),
        "direction": fields.Number(required=False),
        "page_section": fields.List(fields.Dict, required=False)
    })
    def put(self, id, **kwargs):
        """页面修改
          ---

          tags:
            - 页面
          parameters:
            - name: id
              in: body
              type: string
              required: true
        """
        page = db.session.query(Page).filter(Page.id == id).first()

        page.title = kwargs.get("title")
        page.type = PageSection.string_to_data_type(kwargs.get("type"))
        page.direction = Page.string_to_direction_type(kwargs.get("direction", 1))

        sections = kwargs.get("page_section")
        if sections or len(sections) > 0:
            for i, item in enumerate(sections):
                old_section = db.session.query(PageSection).filter(PageSection.id == item.get("id")).first()
                if not old_section:
                    continue
                old_section.title = item.get("title")
                old_section.entity_id = item.get("entity_id")
                old_section.entity_params = item.get("entity_params")
                old_section.section_type = PageSection.string_to_data_type(item.get("section_type"))
                old_section.sort = i
                old_section.nodes = item.get("nodes")

                db.session.add(old_section)

        db.session.add(page)
        db.session.commit()

        return json_response(message="修改成功")

    def get(self, id):
        """获取页面详情
          ---
          tags:
            - 页面
          parameters:
            - name: id
              in: body
              type: string
              required: true
        """
        page = db.session.query(Page).filter(Page.id == id).first()
        if not page:
            return json_response(message="找不到页面", status=404)

        return json_response(data=self.page_schema.dump(page).data)


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
