from marshmallow import fields, Schema
from flask_apispec import use_kwargs
from extensions import db
from arrplat.resources.organization.models import Organization
from .models import OrgApplication

from flask_restful import Resource
from .models import Application, ApplicationMenus
from arrplat.common.utils import json_response, generate_uuid_len, valid_uuid, valid_phone, valid_boolean
from arrplat.resources.application.schema import ApplicationSchema
from arrplat.resources.page.models import Page, PageSection, DataSource
from arrplat.resources.share.models import SharePage
from arrplat.resources.page.schema import DataSourceSchema, PageSchema, PageSectionSchema
from arrplat.resources.share.schema import SharePageSchema
import time


class DataSourceListResource(Resource):
    data_source_schema = DataSourceSchema(many=True)

    def get(self, app_id):
        """查询轻应用数据源
          ---

          tags:
            - 轻应用
          parameters:
            - name: id
              in: body
              type: string
              required: true
        """
        data_source = db.session.query(DataSource).filter(DataSource.application_id == app_id)
        if not data_source:
            return json_response(message="找不到数据源", status=404)

        data = self.data_source_schema.dump(data_source).data
        return json_response(data)


class PageSectionResource(Resource):
    def delete(self, page_id, section_id):
        """页面段落删除
          ---

          tags:
            - 轻应用
          parameters:
            - name: id
              in: body
              type: string
              required: true
        """
        section = db.session.query(PageSection).filter(PageSection.id == section_id).first()
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
        """页面段落修改
          ---

          tags:
            - 轻应用
          parameters:
            - name: page_id
              in: body
              type: string
              required: true
        """
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
    share_page_schema = SharePageSchema(many=False)

    def delete(self, id):
        """页面删除
          ---

          tags:
            - 轻应用
          parameters:
            - name: id
              in: body
              type: string
              required: true
        """
        page = db.session.query(Page).filter(Page.id == id).first()
        if not page:
            return json_response(message="找不到页面", status=404)

        db.session.delete(page)
        db.session.commit()
        return json_response("删除成功!")

    @use_kwargs({
        "title": fields.String(required=False),
        "type": fields.Number(required=False),
        "direction": fields.String(required=False),
        "config": fields.Dict(required=False),
        "page_section": fields.List(fields.Dict, required=False)
    })
    def put(self, id, **kwargs):
        """页面修改
          ---

          tags:
            - 轻应用
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
        page.config = kwargs.get("config", {})

        sections = kwargs.get("page_section")
        if sections or len(sections) > 0:
            for i, item in enumerate(sections):
                old_section = db.session.query(PageSection).filter(PageSection.id == item.get("id")).first()
                if not old_section:
                    continue
                old_section.title = item.get("title")
                old_section.entity_id = item.get("entity_id")
                old_section.entity_params = item.get("entity_params")
                old_section.section_type = item.get("section_type", None)
                old_section.config = item.get("config", {})
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

        page = self.page_schema.dump(page).data

        share = db.session.query(SharePage).filter(SharePage.page_id == id).first()

        if share:
            page['share'] = self.share_page_schema.dump(share).data

        return json_response(data=page)


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
        "name": fields.String(required=False),
        "title": fields.String(required=True),
        "description": fields.String(required=False),
        "icon": fields.String(required=False),
        "key": fields.String(required=False)
    })
    def put(self, id, **kwargs):
        """应用基本信息修改
          ---

          tags:
            - 轻应用
          parameters:
            - name: id
              in: body
              type: string
              required: true
        """
        if not kwargs or not kwargs.get("title"):
            return json_response(message="参数错误", status=400)

        app = db.session.query(Application).filter(Application.id == id).first()

        if not app:
            return json_response(message=f"未找到应用", status=404)

        app.name = kwargs.get("name")
        app.title = kwargs.get("title")
        app.key = kwargs.get("key")
        app.description = kwargs.get("description")
        app.icon = kwargs.get("icon")

        db.session.add(app)
        db.session.commit()

        return json_response(message="修改成功")

    @use_kwargs({
    })
    def delete(self, id):
        """删除轻应用
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
            description=kwargs.get("description", None),
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
        "config": fields.Dict(required=False),
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
            config=kwargs.get('config', {}),
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
        "name": fields.String(required=True),
        "application_id": fields.String(required=True),
        "type": fields.Number(required=True),
        "icon": fields.String(required=False),
        "link": fields.String(required=False),
        "page_key": fields.String(required=False),
        "parent_id": fields.String(required=False),
        "page_id": fields.String(required=False),
    })
    def post(self, **kwargs):
        app_id = kwargs.get('application_id')
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
              type: number
              required: true
        """
        menu = ApplicationMenus(
            name=kwargs.get('name'),
            application_id=app_id,
            icon=kwargs.get('icon'),
            link=kwargs.get('link'),
            type=ApplicationMenus.string_to_page_type(kwargs.get('type')),
            platform=kwargs.get('platform', 'pc, mobile'),
            sort=kwargs.get('sort', 0),
            parent_id=kwargs.get('parent_id'),
            page_key=kwargs.get('page_key'),
            page_id=kwargs.get('page_id')
        )
        db.session.add(menu)
        db.session.commit()

        return json_response(message="添加成功", data={
            "id": menu.id
        })


class LightAppModifyMenu(Resource):
    @use_kwargs({
        "name": fields.String(required=True),
        "icon": fields.String(required=False),
        "line": fields.String(required=False),
        "type": fields.Number(required=False),
        "page_key": fields.String(required=False),
        "page_id": fields.String(required=False),
        "sort": fields.Number(required=False)
    })
    def put(self, id, **kwargs):
        """菜单修改
          ---

          tags:
            - 轻应用
          parameters:
            - name: id
              in: body
              type: string
              required: true
        """
        if not kwargs or not kwargs.get("name"):
            return json_response(message="参数错误", status=400)

        menu = db.session.query(ApplicationMenus).filter(ApplicationMenus.id == id).first()

        if not menu:
            return json_response(message=f"未找到菜单", status=404)

        menu.name = kwargs.get("name")
        menu.icon = kwargs.get("icon")
        menu.link = kwargs.get("link")
        menu.type = kwargs.get('type', None)
        menu.page_key = kwargs.get("page_key")
        menu.page_id = kwargs.get("page_id")
        menu.sort = kwargs.get("sort", 1)

        db.session.add(menu)
        db.session.commit()

        return json_response(message="修改成功")

    @use_kwargs({
    })
    def delete(self, id):
        """菜单删除
          ---
          tags:
            - 轻应用
          parameters:
            - name: title
              in: body
              type: string
              required: true
        """
        menu = db.session.query(ApplicationMenus) \
            .filter(ApplicationMenus.id == id).first()

        if not menu:
            return json_response(message="找不到菜单", status=404)

        db.session.delete(menu)
        db.session.commit()
        return json_response(message="删除成功")
