import time
from flask_apispec import use_kwargs
from marshmallow import fields
from flask_restful import Resource

from extensions import db
from arrplat.common.auth_jwt_utils import user_required
from arrplat.common.pagination import paginate
from arrplat.common.utils import json_response, generate_uuid, valid_uuid, valid_phone, valid_boolean
from arrplat.resources.application.models import Application, OrgApplication, Message, ApplicationMenus
from arrplat.resources.application.schema import OrgApplicationSchema, ApplicationSchema
from arrplat.resources.auth.models import OrgStaffRole, OrgAuthPowerConfig, OrgRoleConfig, OrgRolePower
from arrplat.resources.auth.schema import OrgAuthPowerConfigSchema, OrgRoleConfigSchema
from arrplat.resources.auth.sms_utils import send_sms
from arrplat.resources.organization.models import Organization, OrgStaff, OrgDepartment, OrgDepartmentStaff, OrgRequest
from flask_jwt_extended import get_current_user
from arrplat.resources.organization.schema import OrganizationSchema, OrgStaffSchema, OrgDepartmentSchema
from arrplat.resources.user.models import User, UserInfo
from arrplat.config import config, DEFAULT_PAGE, DEFAULT_PAGE_SIZE
from .services import add_staff_role, add_staff_department


class OrganizationResource(Resource):
    @user_required
    def get(self, org_id):
        """获取组织信息
          ---
          tags:
            - 组织
          parameters:
            - name: name
              in: url
              type: string
              required: true
          responses:
            200:
              description: A list of colors (may be filtered by palette)
              examples:
                response: {"data": null, "message": "修改成功"}
        """
        org_obj = Organization.query.get_or_404(org_id)
        org_schema = OrganizationSchema(only=('id', 'group_type', 'name', 'address', 'official_company_name',
                                              'official_org_code', 'website', 'description', 'head_url'))
        res = org_schema.dump(org_obj).data
        return json_response(res)

    @use_kwargs({
        "name": fields.String(),
        "address": fields.String(),
        "website": fields.String(),
        "description": fields.String(),
        "head_url": fields.String()
    })
    @user_required
    def put(self, org_id, **kwargs):
        """修改组织信息
          ---
          tags:
            - 组织
          parameters:
            - name: name
              in: json
              type: string
            - name: address
              in: json
              type: string
            - name: website
              in: json
              type: string
            - name: description
              in: json
              type: string
            - name: head_url
              in: json
              type: string
          responses:
            200:
              examples:
                response: {"data": null, "message": "修改成功"}
        """
        if not kwargs:
            return json_response(message="参数不能为空")
        organization = db.session.query(Organization).join(OrgStaff, OrgStaff.org_id == Organization.id).filter(
            Organization.id == org_id, OrgStaff.is_able == 1).first_or_404()
        try:
            for key, value in kwargs.items():
                setattr(organization, key, value)
            db.session.commit()
        except Exception as e:
            _ = e
            db.session.rollback()
            message = "修改失败"
        else:
            message = "修改成功"
        return json_response(message=message)


class OrganizationListResource(Resource):
    @use_kwargs({
        "has_detail": fields.Integer(validate=valid_boolean)
    })
    @user_required
    def get(self, **kwargs):
        """获取加入的组织列表
          ---
          tags:
            - 组织
          parameters:
            - name: has_detail
              in: querystring
              type: int
              description: 是否需要详细的信息 0|1
          responses:
            200:
              description: A list of colors (may be filtered by palette)
              examples:
                response: {"data": [], "message": "ok"}
        """
        has_detail = kwargs.get("has_detail")
        user = get_current_user()
        org_schema = OrganizationSchema(many=True, only=(
            "id", "group_type", "name", "unique_id", "address", "website", "own_user_id",
            "official_company_name", "official_org_code", "description", "head_url"))
        if not has_detail:
            org_list = Organization.query.join(OrgStaff, Organization.id == OrgStaff.org_id).filter(
                OrgStaff.user_id == user.id).all()
            data = org_schema.dump(org_list).data
            return json_response(data=data, message="ok")
        else:
            org_schema.many = False
            org_staff_schema = OrgStaffSchema(
                only=("id", "organization.id", "organization.name", "org_department_staff", "job_title"))

            data = list()
            org_staff_list = db.session.query(Organization, OrgStaff).join(OrgStaff,
                                                                           Organization.id == OrgStaff.org_id).filter(
                OrgStaff.user_id == user.id).all()
            for org, org_staff in org_staff_list:
                org_data = org_schema.dump(org).data
                org_staff_data = org_staff_schema.dump(org_staff).data
                org_data["staff_info"] = org_staff_data
                data.append(org_data)
            return json_response(data=data, message='ok')


class CreateOrganizationResource(Resource):
    @use_kwargs({
        "name": fields.String(required=True),
        "unique_id": fields.String(required=True,
                                   validate=lambda unique_id: True if 2 <= len(unique_id.strip()) <= 32 else False),
        "group_type": fields.String(required=False, validate=lambda group_type: True if group_type in (
            "GOV", "Company", "Personal") else False),
        "address": fields.String(required=False),
        "description": fields.String()
    })
    @user_required
    def post(self, **kwargs):
        """创建组织
          ---
          tags:
            - 组织
          parameters:
            - name: name
              in: body
              type: string
              required: true
            - name: unique_id
              in: body
              type: string
              required: true
            - name: description
              in: body
              type: string
              required: true
            - name: group_type
              in: body
              type: string
              example: GOV Company Personal
            - name: address
              in: body
              type: string
          responses:
            200:
              description: A list of colors (may be filtered by palette)
              examples:
                response: {"data": null, "message": "组织添加成功"}
        """
        unique_id = kwargs.get("unique_id")

        if unique_id:
            exist_unique_id = db.session.query(Organization.id).filter(Organization.unique_id == unique_id).first()
            if exist_unique_id:
                return json_response(message="组织ID已经存在", status=403)

        user = get_current_user()
        org_id = generate_uuid()
        org_department_id = generate_uuid()
        staff_id = generate_uuid()

        organization = Organization()
        for key, value in kwargs.items():
            setattr(organization, key, value)
        organization.own_user_id = user.id
        organization.id = org_id

        org_staff = OrgStaff(
            id=staff_id,
            org_id=org_id,
            user_id=user.id,
            job_title="组织创建人"
        )

        org_department = OrgDepartment(
            id=org_department_id,
            org_id=org_id,
            name="大本营"
        )

        org_department_staff = OrgDepartmentStaff(
            org_department_id=org_department_id,
            staff_id=staff_id
        )

        result = db.session.query(Application.id).filter(Application.title == "组织管理").first()
        org_application = None
        if result:
            org_application = OrgApplication(
                application_id=result.id,
                organization_id=org_id,
                status=1
            )

        try:
            db.session.add(organization)
            db.session.add(org_department)
            db.session.add(org_staff)
            db.session.add(org_department_staff)
            if org_application:
                db.session.add(org_application)
            db.session.commit()
        except Exception as e:
            _ = e
            print(e)
            db.session.rollback()
            return json_response(message="组织添加失败", status=403)
        else:
            return json_response(message="组织添加成功")


class OrgDepartmentResource(Resource):
    @user_required
    def get(self, org_id, org_department_id):
        """组织部门信息获取
          ---
          tags:
            - 组织部门
          parameters:
            - name: org_id
              in: url
              type: string
              required: true
              description: 组织id
            - name: org_department_id
              in: url
              type: string
              required: true
              description: 部门id
          responses:
            200:
              description: A list of colors (may be filtered by palette)
              examples:
                response: {"data": {}, "message": "ok"}
        """
        user = get_current_user()
        org_staff = db.session.query(OrgStaff.id).filter(OrgStaff.user_id == user.id, OrgStaff.org_id == org_id).first()
        if not org_staff:
            return json_response(message="您不属于该组织", status=403)
        org_department = OrgDepartment.query.filter_by(id=org_department_id).first_or_404()

        org_department_schema = OrgDepartmentSchema()
        data = org_department_schema.dump(org_department).data
        return json_response(data=data, message="ok")

    @use_kwargs({
        "name": fields.String(),
        "parent_id": fields.String(validate=valid_uuid)
    })
    @user_required
    def put(self, org_id, org_department_id, **kwargs):
        """组织部门信息修改
          ---
          tags:
            - 组织部门
          parameters:
            - name: org_id
              in: url
              type: string
              required: true
              description: 组织id
            - name: org_department_id
              in: url
              type: string
              required: true
              description: 部门id
            - name: name
              in: body
              type: string
              required: true
              description: 部门名称
            - name: org_department_id
              in: body
              type: string
              required: true
              description: 上级部门id
          responses:
            200:
              description: A list of colors (may be filtered by palette)
              examples:
                response: {"data": null, "message": "修改成功"}
        """
        if not kwargs:
            return json_response(message="参数不能为空", status=403)

        try:
            user = get_current_user()
            org_department = db.session.query(OrgDepartment) \
                .join(OrgStaff, OrgStaff.org_id == OrgDepartment.org_id) \
                .filter(OrgStaff.user_id == user.id, OrgDepartment.id == org_department_id,
                        OrgDepartment.org_id == org_id) \
                .first()

            if org_department:
                name = kwargs.get("name")
                parent_department_id = kwargs.get("parent_id")
                if parent_department_id:
                    parent_department = OrgDepartment.query.filter_by(id=parent_department_id, org_id=org_id).first()
                    if not parent_department:
                        raise Exception("找不到指定的上级部门")
                    if parent_department.parent_id == org_department_id:
                        raise Exception("你选择的上级部门是您的子部门")
                    org_department.parent_id = parent_department_id
                if name:
                    if name == org_department.name:
                        raise Exception("两次的部门名字相同")
                    org_department.name = name
            else:
                raise Exception("找不到该部门")
        except Exception as e:
            message = "修改失败，" + str(e)
            db.session.rollback()
            return json_response(message=message, status=403)
        else:
            db.session.commit()
            return json_response(message="修改成功")

    @user_required
    def delete(self, org_id, org_department_id):
        """部门删除
          ---
          tags:
            - 组织部门
          parameters:
            - name: org_id
              in: url
              type: string
              required: true
              description: 组织id
            - name: org_department_id
              in: url
              type: string
              required: true
              description: 部门id
          responses:
            200:
              description: A list of colors (may be filtered by palette)
              examples:
                response: {"data": null, "message": "删除成功"}
        """
        user = get_current_user()

        org_department = db.session.query(OrgDepartment).join(OrgStaff, OrgStaff.org_id == OrgDepartment.org_id).filter(
            OrgStaff.user_id == user.id, OrgDepartment.id == org_department_id, OrgDepartment.org_id == org_id).first()
        if not org_department:
            return json_response(message="找不到部门", status=404)

        if not org_department.parent_id:
            return json_response(message="根部门无法删除", status=403)

        root_department = OrgDepartment.query.filter_by(org_id=org_id, parent_id=None).first()

        db.session.query(OrgDepartmentStaff).filter(OrgDepartmentStaff.org_department_id == org_department.id).update(
            { OrgDepartmentStaff.org_department_id: root_department.id })

        db.session.query(OrgDepartment).filter(OrgDepartment.parent_id == org_department.id).update(
            { OrgDepartment.parent_id: root_department.id })

        db.session.delete(org_department)
        db.session.commit()
        return json_response(message="部门删除成功，内部员工转到根部门")


class CreateOrgDepartmentResource(Resource):
    @use_kwargs({
        "name": fields.String(required=True, validate=lambda name: True if len(name) >= 2 else False),
        "parent_department_id": fields.String(required=True, validate=valid_uuid)
    })
    @user_required
    def post(self, org_id, **kwargs):
        """创建组织部门
          ---
          tags:
            - 组织部门
          parameters:
             - name: org_id
               in: url
               type: string
             - name: name
               in: url
               type: string
               required: true
               description: 部门名称
             - name: parent_department_id
               in: body
               required: false
               type: string
               description: 上级部门id
          responses:
            200:
              examples:
                response: {"data": null, "message": "ok"}
        """
        user = get_current_user()

        name = kwargs.get("name")
        parent_department_id = kwargs.get("parent_department_id")
        organization = db.session.query(Organization).join(OrgStaff, Organization.id == OrgStaff.org_id) \
            .filter(OrgStaff.user_id == user.id, Organization.id == org_id).first_or_404()

        org_department = OrgDepartment(
            name=name,
            org_id=org_id,
        )
        if parent_department_id:
            parent_department = db.session.query(OrgDepartment.id).filter_by(id=parent_department_id,
                                                                             org_id=organization.id).first()
            if not parent_department:
                return json_response(message="找不到对应的上级部门", status=403)

            org_department.parent_id = parent_department_id

        db.session.add(org_department)
        db.session.commit()
        return json_response(message="添加成功")


class OrgDepartmentListResource(Resource):
    @user_required
    def get(self, org_id):
        """获取组织下的所有部门
          ---
          tags:
            - 组织部门
          parameters:
            - name: org_id
              in: url
              type: string
              required: true
          responses:
            200:
              examples:
                response: {"data": [], "message": "ok"}
        """
        user = get_current_user()
        org_department_list = db.session.query(OrgDepartment) \
            .filter(OrgDepartment.org_id == org_id, OrgStaff.org_id == org_id, OrgStaff.user_id == user.id,
                    OrgDepartment.parent_id.is_(None)) \
            .all()
        org_department_schema = OrgDepartmentSchema(many=True)

        org_department_data = org_department_schema.dump(org_department_list).data

        return json_response(data=org_department_data, message="ok")


class OrgDepartmentStaffListResource(Resource):
    @user_required
    @use_kwargs({
        'page': fields.Integer(),
        'size': fields.Integer()
    })
    def get(self, org_id, org_department_id, **kwargs):
        """获取组织部门雇员列表
          ---
          tags:
            - 组织部门雇员
          parameters:
            - name: org_id
              in: url
              type: string
              required: true
              description: 组织id
            - name: org_department_id
              in: url
              type: string
              required: true
              description: 组织部门id， 如果为-1表示查询组织所有雇员
          responses:
            200:
              description:
              examples:
                response: {"data": [], "message": "ok"}
        """
        page = kwargs.get('page', DEFAULT_PAGE)
        size = kwargs.get('size', DEFAULT_PAGE_SIZE)
        current_user = get_current_user()
        org_staff_query = OrgStaff.query.filter_by(user_id=current_user.id, org_id=org_id, is_able=1)
        if org_department_id != "-1":
            # 自己属于该组织才能查看组织的成员
            org_staff_list = db.session.query(OrgStaff).join(OrgDepartmentStaff).filter(
                org_staff_query.exists(),
                OrgStaff.org_id == org_id,
                OrgDepartmentStaff.org_department_id == org_department_id)
        else:
            org_staff_list = OrgStaff.query.filter(org_staff_query.exists(), OrgStaff.org_id == org_id)

        org_staff_schema = OrgStaffSchema(many=True, only=(
            'id', 'job_title', 'user', 'is_able', 'parent_superior', 'org_staff_role', 'org_department_staff'))
        page_result = paginate(org_staff_list, page, size)
        data = org_staff_schema.dump(page_result.items).data

        return json_response(data=data, message="ok", page=page_result)


class OrgStaffResource(Resource):
    #     @user_required
    @use_kwargs({
        'department_id_list': fields.List(cls_or_instance=fields.String()),
        'job_title': fields.String(required=True),
        'superior_id': fields.String(),
        'role_id_list': fields.List(cls_or_instance=fields.String()),
        'is_able': fields.Integer()
    })
    def put(self, org_id, staff_id, **kwargs):

        org_staff = OrgStaff.query.filter_by(id=staff_id, org_id=org_id, is_able=1).first()
        if not org_staff:
            return json_response(message="找不到该雇员信息", status=404)
        org_staff_schema = OrgStaffSchema(only=("id", "job_title", "user", "is_able", "parent_superior"))

        department_id_list = kwargs.get('department_id_list')
        job_title = kwargs.get('job_title')
        superior_id = kwargs.get('superior_id')
        role_id_list = kwargs.get('role_id_list')
        is_able = kwargs.get('is_able')

        if superior_id:
            superior_obj = OrgStaff.query.filter(OrgStaff.id == superior_id, OrgStaff.org_id == org_id).first()
            if not superior_obj:
                return json_response(None, message='直属人未找到', status=404)

        org_staff.job_title = job_title
        org_staff.superior_id = superior_id
        org_staff.is_able = is_able

        OrgDepartmentStaff.query.filter(OrgDepartmentStaff.staff_id == staff_id).delete()
        OrgStaffRole.query.filter(OrgStaffRole.staff_id == staff_id).delete()

        add_staff_role(role_id_list, staff_id)
        add_staff_department(department_id_list, staff_id)

        db.session.commit()
        return json_response(data={}, message="AAA")

    @use_kwargs({})
    def get(self, org_id, staff_id, **kwargs):
        """组织部门雇员信息
          ---
          tags:
            - 组织部门雇员
          parameters:
            - name: org_id
              in: url
              type: string
              required: true
              description: 组织id
            - name: staff_id
              in: url
              type: string
              required: true
              description: 雇员id
          responses:
            200:
              description: A list of colors (may be filtered by palette)
              examples:
                response: {"data": {}, "message": "ok"}
        """
        org_staff = OrgStaff.query.filter_by(id=staff_id, org_id=org_id, is_able=1).first()
        if not org_staff:
            return json_response(message="找不到该雇员信息", status=404)
        org_staff_schema = OrgStaffSchema(only=("id", "job_title", "user", "is_able", "parent_superior"))

        data = org_staff_schema.dump(org_staff).data
        return json_response(data=data, message="ok")

    @user_required
    def delete(self, org_id, staff_id):
        """退出组织/删除雇员
          ---
          tags:
            - 组织部门雇员
          parameters:
            - name: org_id
              in: url
              type: string
              required: true
              description: 组织id
            - name: staff_id
              in: url
              type: string
              required: true
              description: 雇员id
          responses:
            200:
              examples:
                response: {"data": null, "message": "退出成功"}
        """
        user = get_current_user()
        current_org_staff = db.session.query(OrgStaff.id).filter(OrgStaff.user_id == user.id,
                                                                 OrgStaff.org_id == org_id).first()
        if not current_org_staff:
            return json_response(message="您不属于该组织", status=403)
        org_staff = OrgStaff.query.filter_by(id=staff_id, org_id=org_id).first_or_404()

        if org_staff.job_title == "组织创建人":
            return json_response(message="您是管理员，无法直接退出组织", status=403)
        else:
            db.session.delete(org_staff)
            db.session.commit()
            return json_response(message="退出成功")


class OrgCreateStaffResource(Resource):
    @user_required
    @use_kwargs({
        'phone': fields.String(required=True),
        'department_id_list': fields.List(cls_or_instance=fields.String()),
        'job_title': fields.String(required=True),
        'superior_id': fields.String(),
        'role_id_list': fields.List(cls_or_instance=fields.String()),
        'is_able': fields.Integer()
    })
    def post(self, org_id, **kwargs):
        """组织员工
          ---
          tags:
            - 组织部门雇员
          parameters:
            - name: org_id
              in: url
              type: string
              required: true
              description: 组织ID
            - name: phone
              in: body
              type: string
              required: true
              description: 员工手机号
            - name: department_id_list
              in: body
              type: array
              required: false
              description: 部门ID列表
            - name: job_title
              in: body
              type: string
              required: true
              description: 员工岗位
            - name: superior_id
              in: body
              type: string
              required: true
              description: 直属人ID
            - name: role_id_list
              in: body
              type: array
              required: false
              description: 角色ID列表
            - name: is_able
              in: body
              type: int
              required: false
              description: 是否启用，可以不传，默认为禁用
          responses:
            status:
              description: 返回的状态码信息
              examples:
                response: {'data': null, 'status': {422: '手机号非法', 404: '没有找到直属人',
                200: '发送短信通知加入或者通知邀请', 500: '加入失败', 409: '已存在该组织'}}
                """
        phone = kwargs['phone']
        department_id_list = kwargs.get('department_id_list')
        job_title = kwargs['job_title']
        superior_id = kwargs.get('superior_id')
        role_id_list = kwargs.get('role_id_list')
        is_able = kwargs.get('is_able')

        current_user_obj = get_current_user()

        is_phone = valid_phone(phone)
        if not is_phone:
            return json_response(None, message='手机号非法', status=422)
        superior_obj = None
        if superior_id:
            superior_obj = OrgStaff.query.filter(OrgStaff.id == superior_id, OrgStaff.org_id == org_id).first()
            if not superior_obj:
                return json_response(None, message='直属人未找到', status=404)
        org_obj = Organization.query.get_or_404(org_id)
        user_obj = User.query.filter(User.phone == phone).first()
        if user_obj:
            user_id = user_obj.id
            org_staff_obj = OrgStaff.query.filter(OrgStaff.org_id == org_id, OrgStaff.user_id == user_obj.id).first()
            if org_staff_obj:
                return json_response(None, message='该人员已存在当前组织', status=409)
        else:
            temp_user_id = generate_uuid()
            temp_user_obj = User(
                id=temp_user_id,
                phone=phone,
                nickname=config['system']['USER_DISABLE_NICKNAME_PREFIX'] + phone[-4:],
                create_time=time.time(),
                is_invite_status=1
            )
            temp_user_info_obj = UserInfo(
                user_id=temp_user_id,
            )

            org_req_obj = OrgRequest(
                sender_id=current_user_obj.id,
                message='邀请您到我们的组织',
                create_time=time.time(),
                org_id=org_id
            )
            db.session.add_all([temp_user_obj, temp_user_info_obj, org_req_obj])
            user_id = temp_user_id

        staff_uuid = generate_uuid()
        # 已注册 发短信通知，直接拉进来
        org_staff_obj = OrgStaff(
            id=staff_uuid,
            user_id=user_id,
            job_title=job_title,
            is_able=is_able if is_able in [0, 1] else 0,
            superior_id=superior_obj.id if superior_obj else None,
            org_id=org_id
        )
        db.session.add(org_staff_obj)
        add_staff_role(role_id_list, staff_uuid)
        add_staff_department(department_id_list, staff_uuid)
#         if department_id_list:
#             for dep in department_id_list:
#                 org_dep_obj = OrgDepartmentStaff(
#                     org_department_id=dep,
#                     staff_id=staff_uuid
#                 )
#                 db.session.add(org_dep_obj)
#         if role_id_list:
#             for role in role_id_list:
#                 staff_role_obj = OrgStaffRole(
#                     staff_id=staff_uuid,
#                     org_role_config_id=role
#                 )
#                 db.session.add(staff_role_obj)
        message_obj = Message(
            title='邀请信息',
            content=f'{current_user_obj.nickname}邀请您加入组织:{org_obj.name}',
            send_time=time.time(),
            message_type=4,  # 邀请消息
            organization_id=org_obj.id,
            user_id=user_id
        )
        db.session.add(message_obj)
        s = send_sms(generate_uuid(), phone, "锐途云", "SMS_181866455",
                     {'name': f'{current_user_obj.nickname}', 'org': f'{org_obj.name}'})
        print(s)
        try:
            db.session.commit()
            return json_response(None, message='加入成功，将以短信形式通知该员工', status=200)
        except Exception as e:
            _ = e
            db.session.rollback()
            return json_response(None, message=f'加入失败，{e}', status=500)
        #
        #
        # else:
        #
        #     # return json_response(None, message='该用户未注册，将以短信的形式对其通知', status=200)
        #     # except Exception as e:
        #     #     _ = e
        #     #     db.session.rollback()
        #     #     return json_response(None, message=f'该用户未注册，短信发送失败{e}', status=500)


class OrgAuthMenuResource(Resource):
    def get(self, org_id):
        """功能菜单
         ---
         tags:
           - 权限、功能

         responses:
           200:
             description:
             examples:
               response: {"data": {"system_menu": "", "application_menu": ""}, "message": "ok"}
               """
        base_query = OrgAuthPowerConfig.query.filter(OrgAuthPowerConfig.parent_id == None)
        system_auth_menu_obj = base_query.filter(OrgAuthPowerConfig.type == 0).all()
        application_auth_menu_obj = base_query.filter(OrgAuthPowerConfig.type == 1).join(Application,
                                                                                         OrgApplication).filter(
            OrgApplication.organization_id == org_id).all()
        org_auth_power_config_schema = OrgAuthPowerConfigSchema(many=True)
        sys_res = org_auth_power_config_schema.dump(system_auth_menu_obj).data
        application_res = org_auth_power_config_schema.dump(application_auth_menu_obj).data
        res = {'system_menu': sys_res, 'application_menu': application_res}
        return json_response(res, message='查询成功')


class OrgRoleResource(Resource):
    def get(self, org_id):
        """角色列表
          ---
          tags:
           - 权限、功能
          parameters:
            - name: org_id
              in: body
              type: path
              required: true
          responses:
            200:
              description:
              examples:
                response: {"data": "data", "message": "ok"}
        """
        org_role_obj = OrgRoleConfig.query.filter(OrgRoleConfig.org_id == org_id).order_by(
            OrgRoleConfig.create_time.desc()).all()
        org_role_config_schema = OrgRoleConfigSchema(many=True)
        res = org_role_config_schema.dump(org_role_obj).data
        return json_response(res, message='查询成功', status=200)

    @use_kwargs({
        'name': fields.String(required=True),
    })
    def post(self, org_id, **kwargs):
        """创建角色
                 ---
                 tags:
                   - 权限、功能
                 parameters:
                   - name: org_id
                     in: body
                     type: path
                     required: true
                   - name: name
                     in: body
                     type: string
                     required: true
                 responses:
                   200:
                     description: 角色名不能重复
                     examples:
                       response: {"data": "data", "message": "ok"}
               """
        name = kwargs['name']

        org_role_config_obj = OrgRoleConfig.query.filter(OrgRoleConfig.name == name,
                                                         OrgRoleConfig.org_id == org_id).first()
        if org_role_config_obj:
            return json_response(None, message='角色已存在', status=409)

        try:
            org_role_config_obj = OrgRoleConfig(
                name=name,
                create_time=time.time(),
                org_id=org_id
            )
            db.session.add(org_role_config_obj)
            db.session.commit()
            return json_response(None, message='角色插入成功')
        except:
            db.session.rollback()
            return json_response(None, message='组织不存在', status=404)


class OrgRoleDetailResource(Resource):
    def delete(self, org_id, role_id):
        """删除角色
         ---
         tags:
           - 权限、功能
         parameters:
           - name: role_id
             in: path
             type: string
             required: true
           - name: org_id
             in: path
             type: string
             required: true
         responses:
           200:
             description:
             examples:
               response: {"data": "data", "message": "ok"}
       """

        org_role_config_obj = OrgRoleConfig.query.filter(OrgRoleConfig.id == role_id).first_or_404()

        db.session.delete(org_role_config_obj)
        db.session.commit()
        return json_response(None, message='角色删除成功')

    @use_kwargs({
        'name': fields.String(required=True)
    })
    def put(self, org_id, role_id, **kwargs):
        """修改角色
         ---
         tags:
           - 权限、功能
         parameters:
           - name: name
             in: body
             type: string
             required: true
           - name: org_id
             in: path
             type: string
             required: true
           - name: role_id
             in: path
             type: string
             required: true
         responses:
           200:
             description: 角色名不能重复
             examples:
               response: {"data": "data", "message": "ok"}
       """
        name = kwargs['name']

        org_role_config_obj = OrgRoleConfig.query.filter(OrgRoleConfig.name == name,
                                                         OrgRoleConfig.org_id == org_id).first()
        if org_role_config_obj:
            return json_response(None, message='该角色名已存在', status=409)
        else:
            org_role_config_obj = OrgRoleConfig.query.filter(OrgRoleConfig.id == role_id).first_or_404()
            org_role_config_obj.name = name
            db.session.commit()
            return json_response(None, message='角色名修改成功')


class OrgAuthRoleStaffResource(Resource):
    @use_kwargs({
        'page': fields.Integer(),
        'size': fields.Integer()
    })
    def get(self, org_id, role_id, **kwargs):
        """角色员工列表
         ---
         tags:
           - 权限、功能
         parameters:
           - name: role_id
             in: path
             type: string
             required: true
           - name: org_id
             in: path
             type: string
             required: true

         responses:
           200:
             description:
             examples:
               response: {"data": "data", "message": "ok"}
       """
        page = kwargs.get('page', DEFAULT_PAGE)
        size = kwargs.get('size', DEFAULT_PAGE_SIZE)

        staff_obj = OrgStaff.query.join(OrgStaffRole, OrgRoleConfig).filter(OrgRoleConfig.org_id == org_id,
                                                                            OrgRoleConfig.id == role_id)
        staff_schema = OrgStaffSchema(many=True, only=(
            'id', 'job_title', 'user', 'is_able', 'parent_superior', 'org_staff_role', 'org_department_staff'))

        page_result = paginate(staff_obj, page, size)
        res = staff_schema.dump(page_result.items).data
        return json_response(data=res, page=page_result)

    @use_kwargs({
        'staff_id': fields.String(required=True)
    })
    def delete(self, org_id, role_id, **kwargs):
        """删除角色员工
                 ---
                 tags:
                   - 权限、功能
                 parameters:
                   - name: role_id
                     in: path
                     type: string
                     required: true
                   - name: org_id
                     in: path
                     type: string
                     required: true
                   - name: staff_id
                     in: body
                     type: string
                     required: true

                 responses:
                   200:
                     description:
                     examples:
                       response: {"data": "data", "message": "ok"}
               """
        staff_id = kwargs['staff_id']
        role_id = role_id

        org_staff_obj = OrgStaffRole.query.filter(OrgStaffRole.staff_id == staff_id,
                                                  OrgStaffRole.org_role_config_id == role_id).first_or_404()
        db.session.delete(org_staff_obj)
        db.session.commit()
        return json_response(None, message='删除成功')

    @use_kwargs({
        'staff_id_list': fields.List(required=True, cls_or_instance=fields.String())
    })
    def put(self, org_id, role_id, **kwargs):
        """修改角色员工
         ---
         tags:
           - 权限、功能
         parameters:
           - name: role_id
             in: path
             type: string
             required: true
           - name: org_id
             in: path
             type: string
             required: true
           - name: staff_id_list
             in: body
             type: array
             required: true

         responses:
           200:
             description:
             examples:
               response: {"data": null, "message": "ok"}
           500:
             examples:
               response: {"data": null, "message": "失败"}
       """
        staff_id_list = kwargs['staff_id_list']
        org_staff_role_obj = OrgStaffRole.query.filter(OrgStaffRole.org_role_config_id == role_id).all()
        left_staff_id_list = [i.staff_id for i in org_staff_role_obj]

        temp_add_obj = list(set(staff_id_list).difference(set(left_staff_id_list)))
        temp_delete_obj = list(set(left_staff_id_list).difference(set(staff_id_list)))

        # 增加
        for item in temp_add_obj:
            temp_add_org_staff_obj = OrgStaffRole(
                staff_id=item,
                org_role_config_id=role_id
            )
            db.session.add(temp_add_org_staff_obj)

        # 删除
        temp_del_org_staff_obj = OrgStaffRole.query.filter(OrgStaffRole.org_role_config_id == role_id,
                                                           OrgStaffRole.staff_id.in_(temp_delete_obj)).all()
        for item in temp_del_org_staff_obj:
            db.session.delete(item)
        try:
            db.session.commit()
            return json_response(None, message='修改成功')
        except Exception as e:
            _ = e
            db.session.rollback()
            return json_response(None, message=f'修改失败{e}', status=500)


class OrgAuthRoleResource(Resource):
    def get(self, org_id, role_id):
        """角色所拥有的功能ID列表
         ---
         tags:
           - 权限、功能
         parameters:
           - name: role_id
             in: path
             type: string
             required: true
           - name: org_id
             in: path
             type: string
             required: true
         responses:
           200:
             description:
             examples:
               response: {"data": "[id_list]", "message": "ok"}
       """
        org_role_power_obj = OrgRolePower.query.filter(OrgRolePower.org_role_id == role_id).join(
            OrgRoleConfig).filter(OrgRoleConfig.org_id == org_id).all()
        res = [i.org_auth_power_config_id for i in org_role_power_obj]

        return json_response(res)

    @use_kwargs({
        'config_id_list': fields.List(cls_or_instance=fields.String(), required=True)
    })
    def put(self, org_id, role_id, **kwargs):
        """修改角色功能
         ---
         tags:
           - 权限、功能
         parameters:
           - name: config_id_list
             in: body
             type: array
             required: true
           - name: role_id
             in: path
             type: string
             required: true
           - name: org_id
             in: path
             type: string
             required: true
         responses:
           200:
             description:
             examples:
               response: {"data": "data", "message": "ok"}
               """
        config_id_list = kwargs['config_id_list']

        # 先删除该角色所有的功能数据
        OrgRolePower.query.filter(OrgRolePower.org_role_id == role_id).delete()

        obj_list = list()
        for item in config_id_list:
            if not item:
                continue
            org_role_power_obj = OrgRolePower(
                org_role_id=role_id,
                org_auth_power_config_id=item
            )
            obj_list.append(org_role_power_obj)
        try:
            db.session.add_all(obj_list)
            db.session.commit()
            return json_response(None, message='修改成功', status=200)
        except:
            db.session.rollback()
            return json_response(None, message='修改失败', status=500)


class OrgApplicationDetailResource(Resource):
    def get(self, org_id, app_id):
        """获取app信息
          ---
          tags:
            - 组织应用
          parameters:
            - name: org_id
              in: path
              type: string
              description:
            - name: app_id
              in: path
              type: string
              description:
          responses:
            200:
              description: A list of colors (may be filtered by palette)
              examples:
                response: {"data": null, "message": "移除成功"}
        """
        app_obj = OrgApplication.query.filter(
            OrgApplication.organization_id == org_id,
            OrgApplication.application_id == app_id,
            OrgApplication.status == 1).first_or_404()
        app_schema = OrgApplicationSchema(only=('id', 'organization_id', 'application_id', 'expire_date',
                                                'status', 'application'))
        res = app_schema.dump(app_obj).data

        return json_response(res)

    @user_required
    def delete(self, org_id, app_id):
        """移除组织应用
          ---
          tags:
            - 组织应用
          parameters:
            - name: org_id
              in: path
              type: string
              description:
            - name: app_id
              in: path
              type: string
              description:
          responses:
            200:
              description: A list of colors (may be filtered by palette)
              examples:
                response: {"data": null, "message": "移除成功"}
        """

        query = db.session.query(Application, OrgApplication).filter(OrgApplication.organization_id == org_id,
                                                                     OrgApplication.application_id == app_id,
                                                                     Application.id == OrgApplication.application_id).first_or_404()
        if query.Application.deletable == 0:
            return json_response(message='该应用不可以删除', status=403)
        else:
            db.session.delete(query.OrgApplication)
            db.session.commit()
        return json_response(message="移除成功")

    @user_required
    def post(self, org_id, app_id):
        """
        组织添加app
          ---
          tags:
            - 组织应用
          parameters:
            - name: org_id
              in: path
              type: string
              description:
            - name: app_id
              in: path
              type: string
              description:
          responses:
            200:
              description:
              examples:
                response: {"data": [], "message": "ok"}
            500:
              examples:
                response: {"message": "添加失败"}
        """
        org_app_obj = OrgApplication.query.filter(OrgApplication.organization_id == org_id,
                                                  OrgApplication.application_id == app_id).first()
        if org_app_obj:
            return json_response(None, message='该组织下已存在该应用', status=409)
        else:
            org_app_obj = OrgApplication(
                organization_id=org_id,
                application_id=app_id,
                status=1
            )

            db.session.add(org_app_obj)
            try:
                db.session.commit()

                return json_response(None, message='添加成功')
            except Exception as e:
                _ = e
                db.session.rollback()
                return json_response(None, message=f'添加失败{_}', status=500)


class OrgApplicationResource(Resource):
    @use_kwargs({
        'is_all': fields.Integer(required=False),
        'platform': fields.String(required=False)
    })
    def get(self, org_id, **kwargs):
        """app列表
          ---
          tags:
            - 组织应用
          parameters:
            - name: is_all
              in: query string
              type: boolean
              description: 是否全部app
            - name: org_id
              in: path
              type: string
              description: 是否全部app
            - name: platform
              in: query string
              type: string
              description: 菜单类型 mobile or pc
          responses:
            200:
              description:
              examples:
                response: {"data": [], "message": "ok"}
        """
        is_all = kwargs.get('is_all')
        platform = kwargs.get('platform', 'pc')
        if is_all:
            org_obj = Application.query.join(ApplicationMenus, isouter=True).filter(
                ApplicationMenus.platform.contains(platform)).order_by(Application.sort.asc()).all()
            org_schema = ApplicationSchema(many=True, platform=platform)
            res = org_schema.dump(org_obj).data

            # 查询出该组织下的所有app
            org_app_obj = OrgApplication.query.filter(OrgApplication.organization_id == org_id).all()
            self_org_app_list_id = [i.application_id for i in org_app_obj]
            # 更新返回数据是否已被该组织所有
            for item in res:
                if item['id'] in self_org_app_list_id:
                    item.update({'is_install': 1})
                else:
                    item.update({'is_install': 0})

            # return json_response(res)
        else:
            # 查询出该组织下的所有app
            print('platform:')
            print(platform)

            org_app_obj = Application.query.join(OrgApplication) \
                .filter(OrgApplication.organization_id == org_id) \
                .join(ApplicationMenus, isouter=True) \
                .filter(ApplicationMenus.platform.like('%' + platform + '%')) \
                .order_by(Application.sort.asc()).all()
            org_schema = ApplicationSchema(many=True, platform=platform)
            res = org_schema.dump(org_app_obj).data
            # return json_response(res)

        # 重新整理menus结构
        for org_app in res:
            menus = org_app.get('menus', [])
            # 按照sort排序
            menus.sort(key=lambda x: x['sort'], reverse=False)

            # 先把父节点拿出来
            parent_menus = [x for x in menus if x.get('parent_id', '0') == '0']
            # print(parent_menus)

            # 补充子节点
            for m in parent_menus:
                m['children'] = []
                # 必须用倒序遍历, 否则remove会漏数据
                for n in menus[::-1]:
                    # print(n)
                    if n['parent_id'] == m['id']:
                        # 因为倒序遍历, 要用insert保证顺序, 否则用append
                        m['children'].insert(0, n)
                        menus.remove(n)
        return json_response(res)
