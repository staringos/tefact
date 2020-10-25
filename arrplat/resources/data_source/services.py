from .models import DataSource
from extensions import db
from arrplat.resources.organization.services import org_exists
from arrplat.resources.organization.models import OrgStaff
from arrplat.common.utils import json_response


def allow_access_data_source(id, user_id):
    if not id:
        return json_response(message="参数错误", status=400)

    data_source = db.session.query(DataSource).filter(DataSource.id == id).first()

    org = org_exists(data_source.org_id)

    if not org:
        return json_response(message=f"组织ID错误", status=403)

    staff = db.session.query(OrgStaff).filter(OrgStaff.user_id == user_id and OrgStaff.org_id == org.id).first()

    if not staff:
        return json_response(message=f"用户无权限", status=403)

    return data_source
