"""An example of using kubetest to manage a deployment."""

import os
import pytest
import time

@pytest.mark.applymanifests('data', files=[
    'test_deploy_lamp.yaml',
])

def test_deployment(kube):

    # Wait for the objects registered via marker to be ready.
    kube.wait_for_registered(timeout=120)
    time.sleep(10)

    print("deployment.yaml :")

## NAMESPACES
    namespaces = kube.get_namespaces()
    assert "lamp-client" in namespaces

## SECRETS
    secrets = kube.get_secrets(namespace='lamp-client')
    print("secrets :", end=" ")
    for secret in secrets:
        print(secret, end=" ")
    print("")

## CONFIGMAP
    configmaps = kube.get_configmaps(namespace='lamp-client')
    assert len(configmaps) == 1 # un seul configmap pour la configuration apache
    print("configmaps :", end=" ")
    for configmap in configmaps:
        print(configmap, end=" ")
    print("")

## PERSISTENT VOLUME
    # get persistent volume
    pv = kube.get_persistentvolume()
    assert len(pv) == 2
    print("persistent volume :", end=" ")
    for persistentvolume in pv:
        print(persistentvolume, end=" ")
    print("")

## PERSISTENT VOLUME CLAIM
    # get persistent volume claim
    pvc = kube.get_persistentvolumeclaim(namespace='lamp-client')
    assert len(pv) == 2
    print("persistent volume :", end=" ")
    for persistentvolumeclaim in pvc:
        print(persistentvolumeclaim, end=" ")
    print("")

## DEPLOYMENTS

    # get my deployment in namespace
    deployments = kube.get_deployments(namespace='lamp-client')
    assert deployments is not None # existance du déploiment dans le namespace indiqué
    print("deployments :", end=" ")
    for deployment in deployments:
        print(deployment, end=" ")
    print("")

## PODS

    # get pods
    pods = kube.get_pods(namespace='lamp-client')
    assert len(pods) == 2 # un pod apache-php et un pod mariadb
    print("pods :", end=" ")
    for pod in pods:
        print(pod, end=" ")
    print("")

## SERVICES

    services = kube.get_services(namespace='lamp-client')
    assert len(services) == 2 # un pour apache et un pour mariadb
    print("services :", end=" ")
    for service in services:
        print(service, end=" ")
    print("")
