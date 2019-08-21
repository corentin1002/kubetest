"""An example of using kubetest to manage a deployment."""

import os
import pytest
import time

@pytest.mark.applymanifests('configs', files=[
    'deployment.yaml',
    'deployment-1.yaml'
])

def test_deployment(kube):

    # Wait for the objects registered via marker to be ready.
    kube.wait_for_registered(timeout=30)
    time.sleep(10)

    print("deployment.yaml :")

## NAMESPACES
    namespaces = kube.get_namespaces()
    assert "lamp-client" in namespaces

## SECRET
    secrets = kube.get_secrets(namespace='lamp-client')
    assert len(secrets) == 4
    print("secrets :")
    for secret in secrets:
        print(secret)

## CONFIGMAP

    configmaps = kube.get_configmaps(namespace='lamp-client')
    assert len(configmaps) == 1 # un seul configmap pour la configuration apache
    print("configmaps :")
    for configmap in configmaps:
        print(configmap)

## DEPLOYMENTS

    # get my deployment in namespace
    deployments = kube.get_deployments(namespace='lamp-client')
    assert deployments is not None # existance du déploiment dans le namespace indiqué

## PODS

    # get pods
    pods = kube.get_pods(namespace='lamp-client')
    assert len(pods) == 2 # un pod apache-php et un pod mariadb
    print("pods :")
    for pod in pods:
        print(pod)

## SERVICES

    services = kube.get_services(namespace='lamp-client')
    assert len(services) == 2 # un pour apache et un pour mariadb
    print("services :")
    for service in services:
        print(service)


def test_deployment_1(kube):

    # Wait for the objects registered via marker to be ready.
#    kube.wait_for_registered(timeout=30)
#    time.sleep(10)

    print("deployment-1.yaml")

## NAMESPACES
    namespaces = kube.get_namespaces()
    assert "lamp-client-1" in namespaces

## SECRET
    secrets = kube.get_secrets(namespace='lamp-client')
    assert len(secrets) == 4
    print("secrets :")
    for secret in secrets:
        print(secret)

## CONFIGMAP

    configmaps = kube.get_configmaps(namespace='lamp-client-1')
    assert len(configmaps) == 1 # un seul configmap pour la configuration apache
    print("configmaps :")
    for configmap in configmaps:
        print(configmap)

## DEPLOYMENTS

    # get my deployment in namespace
    deployments = kube.get_deployments(namespace='lamp-client-1')
    assert deployments is not None # existance du déploiment dans le namespace indiqué

## PODS

    # get pods
    pods = kube.get_pods(namespace='lamp-client-1')
    assert len(pods) == 2 # un pod apache-php et un pod mariadb
    print("pods :")
    for pod in pods:
        print(pod)

## SERVICES

    services = kube.get_services(namespace='lamp-client-1')
    assert len(services) == 2 # un pour apache et un pour mariadb
    print("services :")
    for service in services:
        print(service)
