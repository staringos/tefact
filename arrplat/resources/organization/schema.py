from marshmallow import fields, post_dump

from arrplat.resources.auth.schema import OrgStaffRoleSchema
from arrplat.resources.organization.models import Organization, OrgStaff, OrgDepartmentStaff, OrgDepartment
from arrplat.resources.user.services import UserSchema
from extensions import ma


class OrganizationSchema(ma.ModelSchema):
    id = fields.String()
    group_type = fields.String()
    name = fields.String()
    address = fields.String()
    official_company_name = fields.String()
    official_org_code = fields.String()

    class Meta:
        model = Organization
        # fields = ('id', 'group_type', 'name', 'address', 'official_company_name', 'official_org_code')


class OrgDepartmentSchema(ma.ModelSchema):
    id = fields.String()
    name = fields.String()
    child_org_departments = fields.Nested('self', many=True)

    class Meta:
        model = OrgDepartment
        fields = ('id', 'name', 'org_id', 'child_org_departments')


class OrgDepartmentStaffSchema(ma.ModelSchema):
    id = fields.String()
    org_department = fields.Nested(OrgDepartmentSchema, only=('id', 'name'))

    class Meta:
        model = OrgDepartmentStaff
        fields = ('id', 'org_department')


class OrgStaffSchema(ma.ModelSchema):
    id = fields.String()
    job_title = fields.String()
    organization = fields.Nested(OrganizationSchema)
    org_department_staff = fields.Nested(OrgDepartmentStaffSchema, many=True, only=('org_department', ))
    # org_department = fields.Nested(OrgDepartmentSchema, only=('id', 'name'))
    user = fields.Nested(UserSchema, only=("id", "head_url", "nickname", "name", "user_info", 'phone'))
    parent_superior = fields.Nested('self', only=("id", "job_title", "is_able", "user"))
    org_staff_role = fields.Nested(OrgStaffRoleSchema, many=True, only=('org_role_config',))

    class Meta:
        model = OrgStaff
        # fields = ('id', 'job_title', 'org_department', 'org_department_staff', 'user')

    @post_dump
    def alter_department(self, data):
        if 'org_department_staff' in data.keys():
            data.update({'org_department': [i['org_department'] for i in data['org_department_staff']]})
            data.pop('org_department_staff')

    @post_dump
    def alter_role_staff(self, data):
        if 'org_staff_role' in data.keys():
            data.update({'role': [i['org_role_config'] for i in data['org_staff_role']]})
            data.pop('org_staff_role')
