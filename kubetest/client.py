"""Test client provided by kubetest for managing Kubernetes objects."""

import logging

from kubernetes import client

from kubetest import objects, utils
from kubetest.condition import Condition, Policy, check_and_sort

log = logging.getLogger('kubetest')


class TestClient:
    """Test client for managing Kubernetes objects.

    Args:
        namespace (str): The namespace associated with the test client.
            Each test case will have its own namespace assigned.
    """

    def __init__(self, namespace):
        self.namespace = namespace

    # ****** Manifest Loaders ******

    @staticmethod
    def load_clusterrolebinding(path):
        """Load a ClusterRoleBinding manifest into a ClusterRoleBinding object.

        Args:
            path (str): The path to the ClusterRoleBinding manifest.

        Returns:
            objects.ClusterRoleBinding: The ClusterRoleBinding for the
                specified manifest.
        """
        log.info('loading clusterrolebinding from path: %s', path)
        clusterrolebinding = objects.ClusterRoleBinding.load(path)
        return clusterrolebinding

    def load_configmap(self, path, set_namespace=True):
        """Load a ConfigMap manifest into a Configmap object.

        By default, this will augment the ConfigMap API Object with
        the generated test case namespace. This behavior can be
        disabled with the `set_namespace` flag.

        Args:
            path (str): The path to the ConfigMap manifest.
            set_namespace (bool): Enable/disable the automatic
                augmentation of the ConfigMap namespace.

        Returns:
            objects.Configmap: The ConfigMap for the specified manifest.
        """
        log.info('loading configmap from path: %s', path)
        configmap = objects.ConfigMap.load(path)
        if set_namespace:
            configmap.namespace = self.namespace
        return configmap

    def load_deployment(self, path, set_namespace=True):
        """Load a Deployment manifest into a Deployment object.

        By default, this will augment the Deployment API Object with
        the generated test case namespace. This behavior can be
        disabled with the `set_namespace` flag.

        Args:
            path (str): The path to the Deployment manifest.
            set_namespace (bool): Enable/disable the automatic
                augmentation of the Deployment namespace.

        Returns:
            objects.Deployment: The Deployment for the specified manifest.
        """
        log.info('loading deployment from path: %s', path)
        deployment = objects.Deployment.load(path)
        if set_namespace:
            deployment.namespace = self.namespace
        return deployment

    def load_pod(self, path, set_namespace=True):
        """Load a Pod manifest into a Pod object.

        By default, this will augment the Pod API Object with
        the generated test case namespace. This behavior can be
        disabled with the `set_namespace` flag.

        Args:
            path (str): The path to the Pod manifest.
            set_namespace (bool): Enable/disable the automatic
                augmentation of the Pod namespace.

        Returns:
            objects.Pod: The Pod for the specified manifest.
        """
        log.info('loading pod from path: %s', path)
        pod = objects.Pod.load(path)
        if set_namespace:
            pod.namespace = self.namespace
        return pod

    def load_rolebinding(self, path, set_namespace=True):
        """Load a RoleBinding manifest into a RoleBinding object.

        By default, this will augment the RoleBinding API Object with
        the generated test case namespace. This behavior can be
        disabled with the `set_namespace` flag.

        Args:
            path (str): The path to the RoleBinding manifest.
            set_namespace (bool): Enable/disable the automatic
                augmentation of the RoleBinding namespace.

        Returns:
            RoleBinding: The RoleBinding for the specified manifest.
        """
        log.info('loading rolebinding from path: %s', path)
        rolebinding = objects.RoleBinding.load(path)
        if set_namespace:
            rolebinding.namespace = self.namespace
        return rolebinding

    def load_secret(self, path, set_namespace=True):
        """Load a Secret manifest into a Secret object.

        By default, this will augment the Secret API Object with
        the generated test case namespace. This behavior can be
        disabled with the `set_namespace` flag.

        Args:
            path (str): The path to the Secret manifest.
            set_namespace (bool): Enable/disable the automatic
                augmentation of the Secret namespace.

        Returns:
            Secret: The Secret for the specified manifest.
        """
        log.info('loading secret from path: %s', path)
        secret = objects.Secret.load(path)
        if set_namespace:
            secret.namespace = self.namespace
        return secret

    def load_service(self, path, set_namespace=True):
        """Load a Service manifest into a Service object.

        By default, this will augment the Service API Object with
        the generated test case namespace. This behavior can be
        disabled with the `set_namespace` flag.

        Args:
            path (str): The path to the Service manifest.
            set_namespace (bool): Enable/disable the automatic
                augmentation of the Service namespace.

        Returns:
            Service: The Service for the specified manifest.
        """
        log.info('loading service from path: %s', path)
        service = objects.Service.load(path)
        if set_namespace:
            service.namespace = self.namespace
        return service

    # ****** Generic Helpers on ApiObjects ******

    def create(self, obj):
        """Create the provided API Object on the Kubernetes cluster.

        If the object does not already have a namespace assigned to it,
        the client's generated test case namespace will be used.

        Args:
            obj (objects.ApiObject): A kubetest API Object wrapper.
        """
        if obj.namespace is None:
            obj.namespace = self.namespace

        obj.create()

    def delete(self, obj, options=None):
        """Delete the provided API Object from the Kubernetes cluster.

        If the object does not already have a namespace assigned to it,
        the client's generated test case namespace will be used.

        Args:
            obj (objects.ApiObject): A kubetest API Object wrapper.
            options (client.V1DeleteOptions): Additional options for
                deleting the API Object from the cluster.
        """
        if obj.namespace is None:
            obj.namespace = self.namespace
        if options is None:
            options = client.V1DeleteOptions()

        obj.delete(options=options)

    @staticmethod
    def refresh(obj):
        """Refresh the underlying Kubernetes API Object status and state.

        Args:
            obj (objects.ApiObject): A kubetest API Object wrapper.
        """
        obj.refresh()

    # ****** General Helpers ******

    def get_deployments(self, fields=None, labels=None):
        """Get Deployments under the test case namespace.

        Args:
            fields (dict[str, str]): A dictionary of fields used to restrict
                the returned collection of Deployments to only those which match
                these field selectors. By default, no restricting is done.
            labels (dict[str, str]): A dictionary of labels used to restrict
                the returned collection of Deployments to only those which match
                these label selectors. By default, no restricting is done.

        Returns:
            dict[str, objects.Deployment]: The Deployments, where the key is
                the Deployment name and the value is the Deployment.
        """
        selectors = utils.selector_kwargs(fields, labels)

        deployment_list = client.AppsV1Api().list_namespaced_deployment(
            namespace=self.namespace,
            **selectors,
        )

        deployments = {}
        for obj in deployment_list.items:
            deployment = objects.Deployment(obj)
            deployments[deployment.name] = deployment

        return deployments

    def get_configmaps(self, fields=None, labels=None):
        """Get ConfigMaps under the test case namespace.

        Args:
            fields (dict[str, str]): A dictionary of fields used to restrict
                the returned collection of ConfigMaps to only those which match
                these field selectors. By default, no restricting is done.
            labels (dict[str, str]): A dictionary of labels used to restrict
                the returned collection of ConfigMaps to only those which match
                these label selectors. By default, no restricting is done.

        Returns:
            dict[str, objects.Configmap]: A dictionary where the key is the
                ConfigMap name and the value is the ConfigMap itself.
        """
        selectors = utils.selector_kwargs(fields, labels)

        configmap_list = client.CoreV1Api().list_namespaced_config_map(
            namespace=self.namespace,
            **selectors,
        )

        configmaps = {}
        for obj in configmap_list.items:
            cm = objects.ConfigMap(obj)
            configmaps[cm.name] = cm

        return configmaps

    def get_pods(self, fields=None, labels=None):
        """Get Pods under the test case namespace.

        Args:
            fields (dict[str, str]): A dictionary of fields used to restrict
                the returned collection of Pods to only those which match
                these field selectors. By default, no restricting is done.
            labels (dict[str, str]): A dictionary of labels used to restrict
                the returned collection of Pods to only those which match
                these label selectors. By default, no restricting is done.

        Returns:
            dict[str, objects.Pod]: A dictionary where the key is the Pod
                name and the value is the Pod itself.
        """
        selectors = utils.selector_kwargs(fields, labels)

        pod_list = client.CoreV1Api().list_namespaced_pod(
            namespace=self.namespace,
            **selectors,
        )

        pods = {}
        for obj in pod_list.items:
            pod = objects.Pod(obj)
            pods[pod.name] = pod

        return pods

    def get_services(self, fields=None, labels=None):
        """Get Services under the test case namespace.

        Args:
            fields (dict[str, str]): A dictionary of fields used to restrict
                the returned collection of Services to only those which match
                these field selectors. By default, no restricting is done.
            labels (dict[str, str]): A dictionary of labels used to restrict
                the returned collection of Services to only those which match
                these label selectors. By default, no restricting is done.

        Returns:
            dict[str, objects.Service]: A dictionary where the key is the
                Service name and the value is the Service itself.
        """
        selectors = utils.selector_kwargs(fields, labels)

        service_list = client.CoreV1Api().list_namespaced_service(
            namespace=self.namespace,
            **selectors,
        )

        services = {}
        for obj in service_list.items:
            service = objects.Service(obj)
            services[service.name] = service

        return services

    # ****** Test Helpers ******

    @staticmethod
    def wait_for_conditions(*args, timeout=None, interval=1, policy=Policy.ONCE):
        """Wait for all of the provided Conditions to be met.

        All Conditions must be met for this to unblock. If no Conditions are
        provided, this method will do nothing.

        Args:
            *args (Condition): Conditions to check.
            timeout (int): The maximum time to wait, in seconds, for the
                provided Conditions to be met. If all of the Conditions are
                not met within the given timeout, this will raise a TimeoutError.
                By default, there is no timeout so this will wait indefinitely.
            interval (float|int): The time, in seconds, to sleep before
                re-evaluating the conditions. Default: 1s
            policy (condition.Policy): The condition checking policy that defines
                the checking behavior. Default: ONCE

        Raises:
            TimeoutError: The Conditions were not met within the specified
                timeout period.
            ValueError: Not all arguments are a Condition.
        """
        # If no Conditions were given, there is nothing to do.
        if not args:
            return

        # If something was given, make sure they are all Conditions
        if not all(map(lambda c: isinstance(c, Condition), args)):
            raise ValueError('All arguments must be a Condition')

        # make a copy of the conditions
        to_check = list(args)

        def condition_checker(conditions):
            # check that the conditions were met according to the
            # condition checking policy
            met, unmet = check_and_sort(*conditions)
            if policy == Policy.ONCE:
                log.info('check met: %s', met)
                conditions[:] = unmet
                return len(unmet) == 0

            elif policy == Policy.SIMULTANEOUS:
                return len(unmet) == 0 and len(met) == len(args)

            else:
                raise ValueError(
                    'Invalid condition policy specified: {}'.format(policy)
                )

        wait_condition = Condition(
            'wait for conditions to be met',
            condition_checker,
            to_check,
        )

        utils.wait_for_condition(
            condition=wait_condition,
            timeout=timeout,
            interval=interval,
        )
