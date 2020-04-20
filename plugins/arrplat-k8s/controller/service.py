from flask_jwt_extended import get_current_user

from .models import Cluster
from .k8s import Kubernetes
from extensions import db
from arrplat.resources.organization.models import OrgStaff, Organization, User


def valid_env(env):
    for index, item in enumerate(env):
        if "name" in item and "value" in item:
            env[index] = {
                "name": item["name"],
                "value": item["value"]
            }
            continue
        else:
            return list()
    return env


def valid_deployment_ports(ports):
    for index, item in enumerate(ports):
        if "containerPort" in item and "protocol" in item:
            protocol = item["protocol"]
            containerPort = item["containerPort"]
            if 0 <= containerPort <= 65535 and protocol in ["TCP", "UDP"]:
                ports[index] = {
                    "containerPort": containerPort,
                    "protocol": protocol
                }
                continue
        return list()
    return ports


def valid_service_ports(ports):
    for index, item in enumerate(ports):
        if "port" in item and "targetPort" in item and "protocol" in item:
            protocol = item["protocol"]
            port = item["port"]
            targetPort = item["targetPort"]
            if 0 <= targetPort < 65535 and 0 <= port < 65535 and protocol in ["TCP", "UDP"]:
                ports[index] = {
                    "protocol": protocol,
                    "port": port,
                    "targetPort": targetPort,
                }
                continue
        return list()
    return ports


def format_ingress_rules(rules):
    data = list()
    for rule in rules:
        temp_rule = dict()
        temp_rule["host"] = rule.host
        temp_rule["http_paths"] = list()
        for path in rule.http.paths:
            temp_rule["http_paths"].append({
                "path": path.path,
                "backend":{
                    "service_port":  path.backend.service_port,
                    "service_name":  path.backend.service_name,
                }
            })
        data.append(temp_rule)
    return data


def get_k8s(cluster_id):
    user = get_current_user()
    cluster = db.session.query(Cluster).join(Organization, OrgStaff, User).filter(
        Cluster.id == cluster_id, User.id == user.id).first()
    if not cluster:
        raise Exception("找不到该集群")
    server_api = "%s:%d" % (cluster.host, cluster.port)
    k8s = Kubernetes(server_host=server_api, token=cluster.token)
    return k8s
