from flask_apispec import use_kwargs
from flask_restful import Resource
from marshmallow import fields

from flask import make_response, send_from_directory


class PluginsStatic(Resource):
    @use_kwargs({
        'plugins': fields.String(),
        'filename': fields.String()
    })
    def get(self, plugins, filename):
        """下载文件
                  ---
                  tags:
                    - 插件静态文件下载接口

                  parameters:
                    - name: plugins
                      in: url
                      type: string
                      required: true
                      description: 插件名
                    - name: filename
                      in: url
                      type: byte
                      required: true
                      description: 文件名
                  responses:
                    200:
                      examples:
                        response: file
                    404:
                      examples:
                        response: not found resource
                """
        directory = '../plugins/{}/static/'.format(plugins)
        res = make_response(send_from_directory(directory=directory, filename=filename, as_attachment=True))
        return res
