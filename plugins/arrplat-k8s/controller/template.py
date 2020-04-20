"""
***Introduce***
name: string
namespace: string
replicas: int
image: string
image_tag: string
ports: sting
    eg:  "[{ containerPort: 80, protocol: "TCP" }]"
env: string
    eg: "[ { name: "NODE_ENV", value: "production" }]"
"""
deployment_template = {
    "apiVersion": "extensions/v1beta1",
    "kind": "Deployment",
    "metadata": {
        "name": "default_name",
        "namespace": "default"
    },
    "spec": {
        "replicas": "1",
        "selector": {
            "matchLabels": {
                "app": "default_name"
            }
        },
        "template": {
            "metadata": {
                "labels": {
                    "app": "default_name"
                }
            },
            "spec": {
                "containers": []
            }
        }
    }
}

service_template = {
    "apiVersion": "v1",
    "kind": "Service",
    "metadata": {
        "name": "default_name",
        "namespace": "default"
    },
    "spec": {
        "selector": {
        },
        "sessionAffinity": "",
        "type": "ClusterIP"
    },
    "status": {
        "loadBalancer": {}
    }
}


ingress_template = {
    "apiVersion": "extensions/v1beta1",
    "kind": "Ingress",
    "metadata": {
        "generation": 1,
        "name": "ingress_name",
        "namespace": "default"
    },
    "spec": {
        "rules": []
    }
}
