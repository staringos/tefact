import os

from flask_apispec import use_kwargs
from marshmallow import fields
from flask_restful import Resource
from arrplat.common.utils import json_response

import json

from arrplat.setup import setup_plugins
from arrplat.config import DEBUG


class PlatformConfig(Resource):
    plugins_config_file = '.arrplat.json'

    @use_kwargs({})
    # @user_required
    def get(self, **kwargs):
        """获取全部APP options列表
          ---
          tags:
            - 平台 - 应用管理
          parameters:
            - name: has_detail
              in: querystring
              type: int
              description: 是否需要详细的信息 0|1
          responses:
            200:
              description: 获取全部平台配置
              examples:
                response: {"data": {}, "message": "ok"}
        """
        with open(self.plugins_config_file, 'r', encoding='utf-8') as f:
            file = json.loads(f.read())
        return json_response(file)

    @use_kwargs({
        'key': fields.String(required=True),
        'config_json': fields.Dict(required=True)
    })
    def put(self, **kwargs):
        """写入插件配置
                  ---
                  tags:
                    - 平台 - 应用管理
                  parameters:
                    - name: key
                      in: body
                      type: string
                      description: 插件key
                    - name: config_json
                      in: body
                      type: json
                      description: 插件配置
                  responses:
                    200:
                      description: 写入成功
                      examples:
                        response: {"data": {}, "message": "ok"}
                    400:
                      description: 写入失败
                      examples:
                        response: {"data": {}, "message": "ok"}
                """
        import json
        key = kwargs['key']
        config_json = kwargs['config_json']
        keys = [i['key'] for i in setup_plugins.plugins_info()['plus_list']]
        if key not in keys:
            return json_response(message='插件key不存在')
        try:
            with open('plugins/{}/arrplus.config.json'.format(key), 'w', encoding="utf-8") as f:
                f.write(json.dumps(config_json, indent=2, ensure_ascii=False))
            return json_response(message='写入成功')
        except Exception as e:
            return json_response(message='写入失败:{}'.format(e), status=400)

    def post(self):
        """重启配置
              ---
              tags:
                - 平台 - 应用管理
              responses:
                400:
                  description: 非debug不可以重启
                  examples:
                    response: {}
        """
        if DEBUG:
            print('开始执行=======')
            try:
                os.system('python restart.py')
            except Exception as e:
                print(f'========={e}')
        else:
            return json_response(message='非debug模式下不可重启', status=400)
