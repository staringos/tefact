from flask_restful import Resource
from arrplat.common.auth_jwt_utils import user_required
from ..models.models import Customer


class CustomerResource(Resource):
    @user_required
    def get(self):
        """获取组织信息
          ---
          tags:
        """
        customer = Customer()
        return "123"
