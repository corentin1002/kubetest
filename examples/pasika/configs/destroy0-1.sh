#!/bin/bash
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
--namespace lamp-client

kubectl delete \
namespace/lamp-client-1 \
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
--namespace lamp-client-1
