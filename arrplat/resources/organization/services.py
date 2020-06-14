from arrplat.resources.organization.models import OrgDepartmentStaff
from arrplat.resources.auth.models import OrgStaffRole
from extensions import db


def add_staff_department(department_id_list, staff_id):
    if department_id_list:
        for dep in department_id_list:
            org_dep_obj = OrgDepartmentStaff(
                org_department_id=dep,
                staff_id=staff_id
            )
            db.session.add(org_dep_obj)


def add_staff_role(role_id_list, staff_id):
    if role_id_list:
        for role in role_id_list:
            staff_role_obj = OrgStaffRole(
                staff_id=staff_id,
                org_role_config_id=role
            )
            db.session.add(staff_role_obj)
