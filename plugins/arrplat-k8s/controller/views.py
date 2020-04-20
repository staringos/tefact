from flask_apispec import use_kwargs
from marshmallow import fields
from flask_restful import Resource
from flask_jwt_extended import get_current_user

from .k8s import Kubernetes
from .models import Cluster
from .schema import ClusterSchema
from .service import get_k8s, valid_env, valid_deployment_ports, valid_service_ports, format_ingress_rules
from extensions import db
from arrplat.config import DEFAULT_PAGE, DEFAULT_PAGE_SIZE
from arrplat.common.auth_jwt_utils import user_required
from arrplat.common.pagination import paginate
from arrplat.common.utils import json_response, valid_uuid, valid_host, generate_random_string
from arrplat.resources.organization.models import OrgStaff, Organization


class ClusterResource(Resource):
    @user_required
    def get(self, cluster_id):
        """获取集群详情
          ---
          tags:
            - 集群
          parameters:
            - name: cluster_id
              in: path
              type: string
              required: true
              description: 集群id
          responses:
            200:
              example:
                response: {"data": {"id":"xx", "host":"https://xxx", "port":6443, "token":"xxx"}, "message": "ok"}
        """
        user = get_current_user()
        cluster = db.session.query(Cluster).join(Organization, OrgStaff).filter(
            Cluster.id == cluster_id,
            OrgStaff.user_id == user.id).first()
        if not cluster:
            return json_response(message="找不到该集群", status=403)

        cluster_schema = ClusterSchema(exclude=("token",))
        data = cluster_schema.dump(cluster).data
        return json_response(data=data)

    @user_required
    @use_kwargs({
        "name": fields.String(validate=lambda name: True if len(name.strip()) >= 2 else False),
        "host": fields.String(validate=valid_host),
        "port": fields.Integer(validate=lambda port: True if 0 < port < 65535 else False),
        "token": fields.String()
    }, locations=("json", ))
    def put(self, cluster_id, **kwargs):
        """修改集群信息
          ---
          tags:
            - 集群
          parameters:
            - name: name
              in: json
              type: string
              required: false
              description: 集群名称
            - name: host
              in: json
              type: string
              required: false
              description: 集群ip地址 https://192.168.1.1
            - name: port
              in: json
              type: int
              required: false
              description: 集群port  6443
            - name: token
              in: json
              type: string
              required: false
          responses:
            200:
              example:
                response: {"data": null, "message": "修改成功"}
        """
        user = get_current_user()
        cluster = db.session.query(Cluster).join(Organization, OrgStaff).filter(
            Cluster.id == cluster_id,
            OrgStaff.user_id == user.id).first()
        if not cluster:
            return json_response(message="找不到该集群", status=403)

        for key, value in kwargs.items():
            setattr(cluster, key, value)
        try:
            db.session.commit()
        except Exception as e:
            _ = e
            db.session.rollback()
            return json_response(message="集群信息修改失败", status=500)
        return json_response(message='集群信息修改成功')


class ClusterListResource(Resource):
    @user_required
    @use_kwargs({
        "org_id": fields.String(required=True, validate=valid_uuid),
        "page": fields.Integer(),
        "page_size": fields.Integer()
    }, locations=("querystring", ))
    def get(self, org_id, **kwargs):
        """获取组织集群列表
          ---
          tags:
            - 集群
          parameters:
            - name: org_id
              in: querystring
              type: string(uuid)
              required: true
              description: 组织id
            - name: page
              in: querystring
              type: int
              required: false
            - name: page_size
              in: querystring
              type: int
              required: false
          responses:
            200:
              example:
                response: {"data": [{"id":"xx", "host":"https://xxx", "port":6443, "token":"xxx"}], "message": "ok"}
        """
        page = kwargs.get("page", DEFAULT_PAGE)
        page_size = kwargs.get("page_size", DEFAULT_PAGE_SIZE)

        user = get_current_user()
        cluster_query = db.session.query(Cluster).join(Organization, OrgStaff).filter(
            OrgStaff.org_id == org_id,
            OrgStaff.user_id == user.id)
        cluster_paginate = paginate(cluster_query, page, page_size)
        cluster_schema = ClusterSchema(many=True, exclude=("token",))
        data = cluster_schema.dump(cluster_paginate.items).data
        return json_response(data, cluster_paginate)

    @user_required
    @use_kwargs({
        "org_id": fields.String(required=True, validate=valid_uuid),
        "name": fields.String(required=True, validate=lambda name: True if len(name.strip()) >= 2 else False),
        "host": fields.String(required=True, validate=valid_host),
        "port": fields.Integer(required=True, validate=lambda port: True if 0 < port < 65535 else False),
        "token": fields.String(required=True)
    }, locations=("json", ))
    def post(self, org_id, name, host, port, token):
        """创建集群
          ---
          tags:
            - 集群
          parameters:
            - name: org_id
              in: json
              type: string
              required: true
              description: 组织id https://192.168.1.1
            - name: name
              in: json
              type: string
              required: true
              description: 集群名称
            - name: host
              in: json
              type: string
              required: true
              description: 集群地址 https://192.168.1.1
            - name: port
              in: json
              type: int
              required: true
              description: 集群端口 6443
            - name: token
              in: json
              type: string
              required: true
          responses:
            200:
              example:
                response: {"data": null, "message": "集群添加成功"}
        """
        user = get_current_user()
        staff_exists = db.session.query(OrgStaff.id).filter_by(user_id=user.id, org_id=org_id).first()
        if not staff_exists:
            return json_response(message="您不是该组织的成员", status=403)

        cluster_exists = db.session.query(Cluster.id).filter_by(org_id=org_id, port=port, host=host).first()
        if cluster_exists:
            return json_response(message="集群已经存在", status=409)

        k8s = Kubernetes(server_host="%s:%d" % (host, port),  token=token)
        try:
            k8s.v1core_app.list_namespace(limit=1)
        except Exception as e:
            _ = e
            return json_response(message="connect failed")

        cluster = Cluster(
            org_id=org_id,
            user_id=user.id,
            name=name,
            host=host,
            port=port,
            token=token
        )

        try:
            db.session.add(cluster)
            db.session.commit()
        except Exception as e:
            _ = e
            db.session.rollback()
            return json_response(message="集群添加失败", status=500)
        else:
            return json_response(message="集群添加成功")


class ClusterDeploymentListResource(Resource):
    @user_required
    @use_kwargs({
        "namespace": fields.String(),
        "limit": fields.Integer()
    }, locations=("querystring", ))
    def get(self, cluster_id, **kwargs):
        """获取组织集群的无状态应用
          ---
          tags:
            - 集群
          parameters:
            - name: namespace
              in: querystring
              type: string
              required: false
              description: 命名空间 default
            - name: limit
              in: querystring
              type: int
              required: false
              description: 数据数量 10
          responses:
            200:
              example:
                response: {"data": [{
                "create_time": "",
                "name": "test-deployment",
                "namespace": "test-namespace",
                "replicas": 2,
                "labels": "test-labels"
            }], "message": "ok"}
        """
        namespace = kwargs.get("namespace")

        try:
            k8s = get_k8s(cluster_id)
        except Exception as e:
            return json_response(message=str(e), status=404)

        if namespace:
            k8s_deployment_list = k8s.v1beta_app.list_namespaced_deployment(**kwargs)
        else:
            k8s_deployment_list = k8s.v1beta_app.list_deployment_for_all_namespaces(**kwargs)
        data = list()
        for item in k8s_deployment_list.items:
            metadata = item.metadata
            data.append({
                "create_time": metadata.creation_timestamp,
                "name": metadata.name,
                "namespace": metadata.namespace,
                "replicas": item.spec.replicas,
                "labels": item.metadata.labels
            })

        return json_response(data=data, message="ClusterDeploymentResource")

    @user_required
    @use_kwargs({
        "name": fields.String(required=True),
        "namespace": fields.String(required=True),
        "image": fields.String(required=True),
        "image_tag": fields.String(required=True),
        "replicas": fields.Integer(required=True),
        "ports": fields.List(cls_or_instance=fields.Dict()),
        "env": fields.List(cls_or_instance=fields.Dict()),
    }, localtion=("json", ))
    def post(self, cluster_id, **kwargs):
        """创建集群无状态应用
          ---
          tags:
            - 集群
          parameters:
            - name: name
              in: json
              type: string
              required: true
              description: deployment的名称
            - name: namespace
              in: json
              type: string
              required: true
              description: 命名空间 default
            - name: image
              in: json
              type: string
              required: true
              description: 镜像 nginx
            - name: image_tag
              in: json
              type: string
              required: true
              description: 镜像版本 1.7
            - name: replicas
              in: json
              type: int
              required: true
              description: 副本数量 2
            - name: ports
              in: json
              type: array
              required: false
              description: '暴露端口号 [{"port":5000, "protocol": "TCP"}, {"port":8080, "protocol": "UDP"}]'
            - name: env
              in: json
              type: array
              required: false
              description: '环境变量 [{"key":PYTHON_ENV, "value": "production"}]'
          responses:
            200:
              example:
                response: {"data": [{
                "create_time": "",
                "name": "test-deployment",
                "namespace": "test-namespace",
                "replicas": 2,
                "labels": "test-labels"
            }], "message": "ok"}
        """
        kwargs["ports"] = valid_deployment_ports(kwargs.get("ports", list()))
        kwargs["env"] = valid_env(kwargs.get("env", list()))

        try:
            k8s = get_k8s(cluster_id)
        except Exception as e:
            return json_response(message=str(e), status=404)

        create_result = k8s.create_deployment(**kwargs)
        status = 200 if create_result["success"] is True else 500
        message = create_result["message"] + " - " + str(create_result.get("error", ""))
        return json_response(message=message, status=status)


class ClusterServiceListResource(Resource):
    @user_required
    @use_kwargs({
        "namespace": fields.String(),
        "limit": fields.Integer()
    })
    def get(self, cluster_id, **kwargs):
        """获取集群service服务列表
          ---
          tags:
            - 集群
          parameters:
            - name: namespace
              in: url
              type: string
              required: false
            - name: limit
              in: querystring
              type: int
              required: false
          responses:
            200:
              example:
                response: {"data": [], "message": "ok"}
        """
        namespace = kwargs.get("namespace")
        try:
            k8s = get_k8s(cluster_id)
        except Exception as e:
            return json_response(message=str(e), status=404)

        if namespace:
            k8s_service_list = k8s.v1core_app.list_namespaced_service(**kwargs)
        else:
            k8s_service_list = k8s.v1core_app.list_service_for_all_namespaces(**kwargs)

        data = list()
        for item in k8s_service_list.items:
            try:
                metadata = item.metadata
                data.append({
                    "create_time": metadata.creation_timestamp,
                    "name": metadata.name,
                    "namespace": metadata.namespace,
                    "labels": item.metadata.labels,
                    "type": item.spec.type,
                    "selector": item.spec.selector,
                    "ports": [port.__dict__ for port in item.spec.ports]
                })
            except Exception as e:
                _ = e
        return json_response(data=data)

    @user_required
    @use_kwargs({
        "name": fields.String(required=True),
        "namespace": fields.String(required=True),
        "deployment_name": fields.String(required=True),
        "ports": fields.List(cls_or_instance=fields.Dict())
    }, locations=("json", ))
    def post(self, cluster_id, **kwargs):
        """新建集群service服务
          ---
          tags:
            - 集群
          parameters:
            - name: name
              in: json
              type: string
              required: true
              description: 集群service名称
            - name: namespace
              in: json
              type: string
              required: true
            - name: deployment_name
              in: json
              type: string
              required: true
              description: 对应的deployment无状态应用的名称
            - name: ports
              in: json
              type: string
              required: false
              description: '外部端口和镜像内部端口的映射 [{"port":80, "targetPort": 80, "protocol": "TCP"}]'
          responses:
            200:
              description: A list of colors (may be filtered by palette)
              example:
                response: {"data": null, "message": "修改成功"}
        """
        kwargs["ports"] = valid_service_ports(kwargs.get("ports"))
        try:
            k8s = get_k8s(cluster_id)
        except Exception as e:
            return json_response(message=str(e), status=404)

        create_result = k8s.create_service(**kwargs)
        status = 200 if create_result["success"] is True else 500
        message = create_result["message"] + " - " + str(create_result.get("error", ""))
        return json_response(message=message, status=status)


class ClusterIngressListResource(Resource):
    @user_required
    @use_kwargs({
        "namespace": fields.String(),
        "limit": fields.Integer()
    }, locations=("querystring", ))
    def get(self, cluster_id, **kwargs):
        """获取集群ingress路由列表
          ---
          tags:
            - 集群
          parameters:
            - name: namespace
              in: querystring
              type: string
              required: false
            - name: limit
              in: querystring
              type: int
              required: false
          responses:
            200:
              example:
                response: {"data": [], "message": "ok"}
        """
        namespace = kwargs.get("namespace")
        try:
            k8s = get_k8s(cluster_id)
        except Exception as e:
            return json_response(message=str(e), status=404)

        if namespace:
            k8s_ingress_list = k8s.v1beta_app.list_namespaced_ingress(**kwargs)
        else:
            k8s_ingress_list = k8s.v1beta_app.list_ingress_for_all_namespaces(**kwargs)

        data = list()
        for item in k8s_ingress_list.items:
            metadata = item.metadata
            data.append({
                "name": metadata.name,
                "namespace": metadata.namespace,
                "create_time": metadata.creation_timestamp,
                "rules": format_ingress_rules(item.spec.rules)
            })

        return json_response(data=data, message="ClusterIngressResource")

    @user_required
    @use_kwargs({
        "name": fields.String(required=True),
        "namespace": fields.String(required=True),
        "host": fields.String(required=True),
        "service_name": fields.String(required=True),
        "service_port": fields.Integer(required=True)
    }, locations=("json", ))
    def post(self, cluster_id, **kwargs):
        """新建集群ingress路由
          ---
          tags:
            - 集群
          parameters:
            - name: name
              in: body
              type: string
              required: true
              description: 路由ingress名称
            - name: namespace
              in: json
              type: string
              required: true
              description: 命名空间
            - name: host
              in: json
              type: string
              required: true
              description: 服务要使用的域名 http://test.com
            - name: service_name
              in: json
              type: string
              required: true
              description: ingress路由对应的集群service名称
            - name: service_port
              in: json
              type: string
              required: true
              description: ingress路由对应的集群service端口号 80
          responses:
            200:
              example:
                response: {"data": null, "message": "ok"}
        """
        try:
            k8s = get_k8s(cluster_id)
        except Exception as e:
            return json_response(message=str(e), status=404)

        create_result = k8s.create_ingress(**kwargs)
        status = 200 if create_result["success"] is True else 500
        message = create_result["message"] + " - " + str(create_result.get("error", ""))
        return json_response(message=message, status=status)


class ClusterWebServerListResource(Resource):
    @user_required
    @use_kwargs({
        "domain": fields.String(required=True),
        "name": fields.String(required=True),
        "namespace": fields.String(required=True),
        "image": fields.String(required=True),
        "image_tag": fields.String(required=True),
        "replicas": fields.Integer(required=True),
        "ports": fields.List(cls_or_instance=fields.Dict()),
        "env": fields.List(cls_or_instance=fields.Dict()),
    })
    def post(self, cluster_id, domain, name, namespace, image, image_tag, replicas, **kwargs):
        """新建一个整套的服务
          ---
          tags:
            - 集群
          parameters:
            - name: domain
              in: body
              type: string
              required: true
              description: 服务配置好的域名
            - name: name
              in: json
              type: string
              required: true
              description: 服务名称
            - name: namespace
              in: json
              type: string
              required: true
              description:
            - name: iamge
              in: json
              type: string
              required: true
              description: 镜像
            - name: iamge_tag
              in: json
              type: string
              required: true
              description: 镜像版本
            - name: replicas
              in: json
              type: int
              required: true
              description: 开启副本个数
            - name: ports
              in: json
              type: string
              required: false
              description: '暴露端口号 [{"port":5000, "protocol": "TCP"}, {"port":8080, "protocol": "UDP"}]'
            - name: env
              in: json
              type: string
              required: false
              description: '环境变量 [{"key":PYTHON_ENV, "value": "production"}]'
          responses:
            200:
              example:
                response: {"data": null, "message": "ok"}
        """
        ports = valid_deployment_ports(kwargs.get("ports", list()))
        env = valid_env(kwargs.get("env", list()))
        try:
            k8s = get_k8s(cluster_id)
        except Exception as e:
            return json_response(message=str(e), status=404)

        random_string = generate_random_string()
        deployment_name = "%s-%s" % (name, random_string)

        create_deployment_result = k8s.create_deployment(
            name=deployment_name,
            namespace=namespace,
            image=image,
            image_tag=image_tag,
            replicas=replicas,
            ports=ports,
            env=env
        )
        status = 200 if create_deployment_result["success"] is True else 500
        message = create_deployment_result["message"] + " - " + str(create_deployment_result.get("error", ""))
        if status != 200:
            return json_response(message=message)

        service_name = "%s-%s-svc" % (name, random_string)
        service_ports = [{"port": item["containerPort"], "targetPort": item["containerPort"], "protocol": item["protocol"]} for item in ports]
        create_service_result = k8s.create_service(
            name=service_name,
            namespace=namespace,
            deployment_name=deployment_name,
            ports=service_ports
        )
        status = 200 if create_service_result["success"] is True else 500
        message = create_service_result["message"] + " - " + str(create_service_result.get("error", ""))
        if status != 200:
            k8s.v1beta_app.delete_namespaced_deployment(deployment_name, namespace)
            return json_response(message=message)

        ingress_name = "%s-%s-ingress" % (name, random_string)
        create_ingress_result = k8s.create_ingress(
            name=ingress_name,
            namespace=namespace,
            host=domain,
            service_name=service_name,
            service_port=service_ports[0]["port"] if service_ports else 80
        )
        status = 200 if create_ingress_result["success"] is True else 500
        message = create_ingress_result["message"] + " - " + str(create_ingress_result.get("error", ""))
        if status != 200:
            k8s.v1beta_app.delete_namespaced_deployment(deployment_name, namespace)
            k8s.v1core_app.delete_namespaced_service(service_name, namespace)
            return json_response(message=message)

        return json_response(message="web service create success")
