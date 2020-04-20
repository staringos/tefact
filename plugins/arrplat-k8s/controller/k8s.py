from copy import deepcopy

from kubernetes import client as kclient

from .template import deployment_template, service_template, ingress_template


class BaseKubernetes(object):

    def __init__(self, server_host, token):
        configuration = kclient.Configuration()
        configuration.host = server_host
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + token, "Content-Type": "application/yaml"}
        configuration.assert_hostname = "k8s-master.novalocal"
        kclient.Configuration.set_default(configuration)

        api_client = kclient.ApiClient(configuration=configuration)
        self.v1beta_app = kclient.ExtensionsV1beta1Api(api_client=api_client)
        self.v1core_app = kclient.CoreV1Api(api_client=api_client)

    def deployment_exists(self, deployment_name, namespace):
        """判断deployment是否已经存在"""
        try:
            self.v1beta_app.read_namespaced_deployment(deployment_name, namespace)
        except Exception as e:
            _ = e
            status = False
        else:
            status = True
        return status

    def service_exists(self, service_name, namespace):
        """服务service是否存在"""
        try:
            self.v1core_app.read_namespaced_service(service_name, namespace)
        except Exception as e:
            _ = e
            status = False
        else:
            status = True
        return status

    def ingress_exists(self, ingress_name, namespace):
        """判断ingress路由是否存在"""
        try:
            self.v1beta_app.read_namespaced_ingress(ingress_name, namespace)
        except Exception as e:
            _ = e
            status = False
        else:
            status = True
        return status

    def get_all_deployment(self, namespace=None):
        """获取所有的deployment"""
        if namespace is None:
            deployment_result = self.v1beta_app.list_deployment_for_all_namespaces()
        else:
            deployment_result = self.v1beta_app.list_namespaced_deployment(namespace=namespace)
        return deployment_result

    def _create_deployment(self, name, namespace: str, body):
        """创建无状态应用deployment"""
        deployment_exists = self.deployment_exists(name, namespace)

        if deployment_exists:
            return {
                "success": False,
                "message": "deployment create failed, deployment is exists!"
            }
        else:
            try:
                created = self.v1beta_app.create_namespaced_deployment(namespace=namespace, body=body, field_manager="Octopus")
            except Exception as e:
                _ = e
                return {
                    "success": False,
                    "message": "deployment create failed, error!",
                    "error": e
                }
            else:
                return {
                    "success": True,
                    "message": "deployment create success!"
                }

    def _create_service(self, name, namespace, body):
        """创建服务service"""
        service_exists = self.service_exists(name, namespace)
        if service_exists:
            return {
                "success": False,
                "message": "service create failed, deployment is exists!"
            }
        else:
            try:
                created = self.v1core_app.create_namespaced_service(namespace=namespace, body=body, field_manager="Octopus")
            except Exception as e:
                _ = e
                return {
                    "success": False,
                    "message": "service create failed, error!"
                }
            else:
                return {
                    "success": True,
                    "message": "service create success!"
                }

    def _create_ingress(self, name, namespace, body):
        """创建路由ingress"""
        ingress_exists = self.ingress_exists(name, namespace)
        if ingress_exists:
            return {
                "success": False,
                "message": "ingress create failed, deployment is exists!"
            }
        else:
            try:
                created = self.v1beta_app.create_namespaced_ingress(namespace=namespace, body=body, field_manager="Octopus")
            except Exception as e:
                _ = e
                return {
                    "success": False,
                    "message": "ingress create failed, error!",
                    "error": e
                }
            else:
                return {
                    "success": True,
                    "message": "ingress creatae success!"
                }


class Kubernetes(BaseKubernetes):
    def create_deployment(self, name, namespace, image, image_tag, replicas=1, ports="", env=""):
        template = deepcopy(deployment_template)

        template["metadata"] = {
            "name": name,
            "namespace": namespace
        }
        template["spec"]["replicas"] = replicas
        template["spec"]["selector"]["matchLabels"]["app"] = name
        template["spec"]["template"]["metadata"]["labels"]["app"] = name
        container = {
            "name": name,
            "image": "%s:%s" % (image, image_tag),
            "imagePullPolicy": "Always",
        }
        if ports:
            container["ports"] = ports
        if env:
            container["env"] = env
        template["spec"]["template"]["spec"]["containers"].append(container)
        return self._create_deployment(name, namespace, body=template)

    def create_service(self, name, namespace, deployment_name, ports=None):
        """

        :param deployment_name:
        :param name:
        :param namespace:
        :param ports: [(port, targetPort), (port1, targetPort1)]
        :return:
        """
        template = deepcopy(service_template)

        template["metadata"]["name"] = name
        template["metadata"]["namespace"] = namespace
        if ports and isinstance(ports, list):
            template["spec"]["ports"] = ports
        template["spec"]["selector"] = {"app": deployment_name}
        return self._create_service('test-ingress', 'arrway', template)

    def create_ingress(self, name, namespace, host, service_name, service_port):
        template = deepcopy(ingress_template)

        template["metadata"]["name"] = name
        template["metadata"]["namespace"] = namespace
        template["spec"]["namespace"] = namespace

        rule = {
            "host": host,
            "http": {
                "paths": [{
                    "backend": {
                        "serviceName": service_name,
                        "servicePort": service_port
                    },
                    "path": "/"
                }]
            }
        }
        template["spec"]["rules"].append(rule)
        return self._create_ingress(name=name, namespace=namespace, body=template)
