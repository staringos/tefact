from marshmallow import fields

from arrplat.resources.application.schema import ApplicationSchema
from arrplat.resources.auth.models import OrgRoleConfig, OrgAuthPowerConfig, OrgStaffRole
from extensions import ma


class OrgRoleConfigSchema(ma.ModelSchema):

    class Meta:
        model = OrgRoleConfig
        # fields = ('id', 'name')


class OrgAuthPowerConfigSchema(ma.ModelSchema):
    children = fields.Nested('self', many=True)
    application = fields.Nested(ApplicationSchema, only=('id', 'name'))

    class Meta:
        model = OrgAuthPowerConfig


class OrgStaffRoleSchema(ma.ModelSchema):
    org_role_config = fields.Nested(OrgRoleConfigSchema, only=('id', 'name'))

    class Meta:
        model = OrgStaffRole
