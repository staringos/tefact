from arrplat.common.utils import json_response
from arrplat.config import config
from qiniu import Auth, put_data
from flask_restful import Resource
from flask import request
import uuid

Conf = config.get('qiniu')


class FileUpload(Resource):

    def post(self, bucket_name='', image_name_to_uuid_handle=True):
        """图片上传接口
          ---
          parameters:
            - name: bucket_name
              in: url
              type: string
              required: true
              description: 篮子名称
            - name: file
              in: body
              type: byte
              required: true
              description: 图片二进制文件
          responses:
            200:
              examples:
                response: {"data": null, "message": "修改成功"}
        """
        # 请求方式 requests.post(url, files={'file': open("/icon/课程表.png", "rb")}).json()
        files = request.files.getlist('file')
        url_list = list()
        bucket_info = Conf.get('info', dict()).get(bucket_name)
        if not bucket_info:
            return json_response(message="找不到指定的bucket!", status=404)
        for file_storage in files:
            file_ext = ''
            if file_storage.filename.find('.') > 0:
                file_ext = file_storage.filename.rsplit('.', 1)[1].strip().lower()
            if file_ext in bucket_info[2]:
                pre_name = str(uuid.uuid1()).replace('-', '') if image_name_to_uuid_handle else \
                    file_storage.filename.rsplit('.', 1)[0].strip().lower()
                file_name = pre_name + '.' + file_ext
                url = self.qiniu_upload_file(file_storage, file_name, bucket_name)
                if url:
                    url_list.append(url)
        return url_list

    @staticmethod
    def upload_files(files, bucket_name='', image_name_to_uuid_handle=True):
        """
        :param files: werkzeug.datastructures.ImmutableMultiDict of instance
        :param bucket_name: bucket_name
        :param image_name_to_uuid_handle:  暂时保留，为Ture时，返回通过uuid处理后的名称(url中为启用此选项)
        :return: list obj
        """
        files = files.getlist('file')
        url_list = list()
        for filestorage in files:
            file_ext = ''
            if filestorage.filename.find('.') > 0:
                file_ext = filestorage.filename.rsplit('.', 1)[1].strip().lower()
            if file_ext in Conf.get('info').get(bucket_name)[2]:
                pre_name = str(uuid.uuid1()).replace('-', '') if image_name_to_uuid_handle else \
                    filestorage.filename.rsplit('.', 1)[0].strip().lower()
                file_name = pre_name + '.' + file_ext
                url = FileUpload.qiniu_upload_file(filestorage, file_name, bucket_name)
                if url:
                    url_list.append(url)
        return url_list

    @staticmethod
    def qiniu_upload_file(source_file, save_file_name, bucket_name='soco'):
        """
        :param bucket_name:  空间名
        :param source_file: FileStorage obj
        :param save_file_name:  filename
        :return: url or None
        # qiniu.put_data方法中的final_data标识符需要改为字节类型(已修改)
        # final_data = '' ==> final_data = b''
        """
        access_key = Conf.get('access_key')
        secret_key = Conf.get('secret_key')
        q = Auth(access_key, secret_key)
        info_d = Conf.get('info')

        token = q.upload_token(info_d[bucket_name][0], save_file_name, 3600)
        try:
            ret, info = put_data(token, save_file_name, source_file.stream.read())
            if info.status_code == 200:
                return '{}/{}'.format(info_d[bucket_name][1], save_file_name)
            return None
        except Exception as e:
            print('{}'.format(e))

    @staticmethod
    def _upload_files(files, bucket_name='', image_name_to_uuid_handle=True):
        """
        :param files: werkzeug.datastructures.ImmutableMultiDict of instance
        :param bucket_name: bucket_name
        :param image_name_to_uuid_handle:  暂时保留，为Ture时，返回通过uuid处理后的名称(url中为启用此选项)
        :return: list obj
        """
        url_list = []
        for filestorage in files:
            file_ext = ''
            if filestorage.filename.find('.') > 0:
                file_ext = filestorage.filename.rsplit('.', 1)[1].strip().lower()
            if file_ext in Conf.get('info').get(bucket_name)[2]:
                pre_name = str(uuid.uuid1()).replace('-', '') if image_name_to_uuid_handle else \
                    filestorage.filename.rsplit('.', 1)[0].strip().lower()
                file_name = pre_name + '.' + file_ext
                url = FileUpload.qiniu_upload_file(filestorage, file_name, bucket_name)
                if url:
                    url_list.append(url)
        return url_list

    @staticmethod
    def qiniu_upload_stream(source_file, save_file_name, bucket_name='soco'):
        """
        :param source_file: FileStorage obj
        :param save_file_name:  filename
        :param bucket_name:  空间名
        :return: url or None
        # qiniu.put_data方法中的final_data标识符需要改为字节类型(已修改)
        # final_data = '' ==> final_data = b''
        """
        access_key = Conf.get('access_key')
        secret_key = Conf.get('secret_key')
        q = Auth(access_key, secret_key)
        info_d = Conf.get('info')

        token = q.upload_token(info_d[bucket_name][0], save_file_name, 3600)
        try:
            ret, info = put_data(token, save_file_name, source_file.stream)
            if info.status_code == 200:
                return '{}/{}'.format(info_d[bucket_name][1], save_file_name)
            return None
        except Exception as e:
            print('{}'.format(e))
