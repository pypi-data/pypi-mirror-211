# ！/usr/bin/env python3
# -*-coding: UTF-8 -*-

from os import path
import yaml
from kubernetes import client, config

config.kube_config.load_kube_config(
    config_file="./keberconfig.yaml")


def create_pod():
    # config.load_kube_config()
    with open(path.join(path.dirname(__file__), "./test_pod.yml")) as f:
        dep = yaml.safe_load(f)
        k8s_core_v1 = client.CoreV1Api()
        resp = k8s_core_v1.create_namespaced_pod(
            body=dep, namespace="default")
        print("Pod created. status='%s'" % resp.metadata.name)

    
def read_pod_status(pod_name: str, namespace: str):
    # config.load_kube_config()
    k8s_core_v1 = client.CoreV1Api()
    return k8s_core_v1.read_namespaced_pod_status(pod_name, namespace)



