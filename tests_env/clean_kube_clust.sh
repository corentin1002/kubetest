#!/bin/bash

export KUBECONFIG="tests_env/kubeconfig-pikdev-unittest-admin.conf"

kubectl delete \
namespace/lamp-client \
service/apache-php \
service/mariadb \
secret/ceph-secret \
secret/user-pass \
secret/regcred2 \
configmap/vhosts-config \
deployment.apps/apache-php \
deployment.apps/mariadb \
deployment.apps/ssh-php \
deployment.apps/proftpd \
persistentvolumeclaim/rbd-pv-claim-cust-db \
persistentvolumeclaim/rbd-pv-claim-cust-www \
--namespace lamp-client

kubectl delete pv rbd-pv-cust-db
kubectl delete pv rbd-pv-cust-www
