"""The test client for managing Kubernetes resources within test cases.

An instance of the ``TestClient`` defined in this module is automatically
created for each test case that uses the ``kube`` fixture. The ``kube``
fixture provides the ``TestClient`` instance to the test case.
"""

import logging

from kubernetes import client

from kubetest import objects, utils
from kubetest.condition import Condition, Policy, check_and_sort

log = logging.getLogger('kubetest')


class TestClient:
    """Test client for managing Kubernetes resources for a test case.

    The ``namespace`` for the TestClient will be automatically generated
    and provided to the TestClient during the test setup process.

    Args:
        namespace (str): The namespace associated with the test
        client.
            Each test case will have its own namespace assigned.
    """

    def __init__(self, namespace):
        self.namespace = namespace
        self.pre_registered = []

    # ****** Manifest Loaders ******

    @staticmethod
    def load_clusterrolebinding(path):
        """Load a manifest YAML into a ClusterRoleBinding object.

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
        """Load a manifest YAML into a ConfigMap object.

        By default, this will augment the ConfigMap object with
        the generated test case namespace. This behavior can be
        disabled with the ``set_namespace`` flag.

        Args:
            path (str): The path to the ConfigMap manifest.
            set_namespace (bool): Enable/disable the automatic
                augmentation of the ConfigMap namespace.

        Returns:
            objects.ConfigMap: The ConfigMap for the specified manifest.
        """
        log.info('loading configmap from path: %s', path)
        configmap = objects.ConfigMap.load(path)
        if set_namespace:
            configmap.namespace = self.namespace
        return configmap

    def load_deployment(self, path, set_namespace=True):
        """Load a manifest YAML into a Deployment object.

        By default, this will augment the Deployment object with
        the generated test case namespace. This behavior can be
        disabled with the ``set_namespace`` flag.

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

    def load_statefulset(self, path, set_namespace=True):
        """Load a manifest YAML into a StatefulSet object.

        By default, this will augment the StatefulSet object with
        the generated test case namespace. This behavior can be
        disabled with the ``set_namespace`` flag.

        Args:
            path (str): The path to the StatefulSet manifest.
            set_namespace (bool): Enable/disable the automatic
                augmentation of the StatefulSet namespace.

        Returns:
            objects.StatefulSet: The StatefulSet for the specified manifest.
        """
        log.info('loading statefulset from path: %s', path)
        statefulset = objects.StatefulSet.load(path)
        if set_namespace:
            statefulset.namespace = self.namespace
        return statefulset

    def load_daemonset(self, path, set_namespace=True):
        """Load a manifest YAML into a DaemonSet object.

        By default, this will augment the DaemonSet object with
        the generated test case namespace. This behavior can be
        disabled with the ``set_namespace`` flag.

        Args:
            path (str): The path to the DaemonSet manifest.
            set_namespace (bool): Enable/disable the automatic
                augmentation of the DaemonSet namespace.

        Returns:
            objects.DaemonSet: The DaemonSet for the specified manifest.
        """
        log.info('loading daemonset from path: %s', path)
        daemonset = objects.DaemonSet.load(path)
        if set_namespace:
            daemonset.namespace = self.namespace
        return daemonset

    def load_pod(self, path, set_namespace=True):
        """Load a manifest YAML into a Pod object.

        By default, this will augment the Pod object with
        the generated test case namespace. This behavior can be
        disabled with the ``set_namespace`` flag.

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
        """Load a manifest YAML into a RoleBinding object.

        By default, this will augment the RoleBinding object with
        the generated test case namespace. This behavior can be
        disabled with the ``set_namespace`` flag.

        Args:
            path (str): The path to the RoleBinding manifest.
            set_namespace (bool): Enable/disable the automatic
                augmentation of the RoleBinding namespace.

        Returns:
            objects.RoleBinding: The RoleBinding for the specified manifest.
        """
        log.info('loading rolebinding from path: %s', path)
        rolebinding = objects.RoleBinding.load(path)
        if set_namespace:
            rolebinding.namespace = self.namespace
        return rolebinding

    def load_secret(self, path, set_namespace=True):
        """Load a manifest YAML into a Secret object.

        By default, this will augment the Secret object with
        the generated test case namespace. This behavior can be
        disabled with the ``set_namespace`` flag.

        Args:
            path (str): The path to the Secret manifest.
            set_namespace (bool): Enable/disable the automatic
                augmentation of the Secret namespace.

        Returns:
            objects.Secret: The Secret for the specified manifest.
        """
        log.info('loading secret from path: %s', path)
        secret = objects.Secret.load(path)
        if set_namespace:
            secret.namespace = self.namespace
        return secret

    def load_service(self, path, set_namespace=True):
        """Load a manifest YAML into a Service object.

        By default, this will augment the Service object with
        the generated test case namespace. This behavior can be
        disabled with the ``set_namespace`` flag.

        Args:
            path (str): The path to the Service manifest.
            set_namespace (bool): Enable/disable the automatic
                augmentation of the Service namespace.

        Returns:
            objects.Service: The Service for the specified manifest.
        """
        log.info('loading service from path: %s', path)
        service = objects.Service.load(path)
        if set_namespace:
            service.namespace = self.namespace
        return service

    def load_PersistentVolume(self, path, set_namespace=False):
        """Load a manifest YAML into a Service object.

        By default, this will augment the Service object with
        the generated test case namespace. This behavior can be
        disabled with the ``set_namespace`` flag.

        Args:
            path (str): The path to the Service manifest.
            set_namespace (bool): Enable/disable the automatic
                augmentation of the Service namespace.

        Returns:
            objects.Service: The Service for the specified manifest.
        """
        log.info('loading persistentvolume from path: %s', path)
        persistentvolume = objects.PersistentVolume.load(path)
        if set_namespace:
            persistentvolume.namespace = self.namespace
        return persistentvolume

    def load_persistentvolumeclaim(self, path, set_namespace=True):
        """Load a manifest YAML into a Service object.

        By default, this will augment the Service object with
        the generated test case namespace. This behavior can be
        disabled with the ``set_namespace`` flag.

        Args:
            path (str): The path to the Service manifest.
            set_namespace (bool): Enable/disable the automatic
                augmentation of the Service namespace.

        Returns:
            objects.Service: The Service for the specified manifest.
        """
        log.info('loading persistentvolumeclaim from path: %s', path)
        persistentvolumeclaim = objects.PersistentVolumeClaim.load(path)
        if set_namespace:
            persistentvolumeclaim.namespace = self.namespace
        return persistentvolumeclaim

    # ****** Generic Helpers on ApiObjects ******

    def create(self, obj):
        """Create the provided ApiObject on the Kubernetes cluster.

        If the object does not already have a namespace assigned to it,
        the client's generated test case namespace will be used.

        Args:
            obj (objects.ApiObject): A kubetest API Object wrapper.
        """
        if obj.namespace is None:
            obj.namespace = self.namespace

        obj.create()

    def delete(self, obj, options=None):
        """Delete the provided ApiObject from the Kubernetes cluster.

        If the object does not already have a namespace assigned to it,
        the client's generated test case namespace will be used.

        Args:
            obj (objects.ApiObject): A kubetest API Object wrapper.
            options (client.V1DeleteOptions): Additional options for
                deleting the resource from the cluster.
        """
        if obj.namespace is None:
            obj.namespace = self.namespace
        if options is None:
            options = client.V1DeleteOptions()

        obj.delete(options=options)

    @staticmethod
    def refresh(obj):
        """Refresh the underlying Kubernetes resource status and state.

        Args:
            obj (objects.ApiObject): A kubetest API Object wrapper.
        """
        obj.refresh()

    # ****** General Helpers ******

    def get_namespaces(self, fields=None, labels=None):
        """Get Namespaces from the cluster.

        Args:
            fields (dict[str, str]): A dictionary of fields used to restrict
                the returned collection of Namespaces to only those which match
                these field selectors. By default, no restricting is done.
            labels (dict[str, str]): A dictionary of labels used to restrict
                the returned collection of Namespaces to only those which match
                these label selectors. By default, no restricting is done.

        Returns:
            dict[str, objects.Namespace]: A dictionary where the key is
            the Namespace name and the value is the Nameself itself.
        """
        selectors = utils.selector_kwargs(fields, labels)

        namespace_list = client.CoreV1Api().list_namespace(
            **selectors,
        )

        namespaces = {}
        for obj in namespace_list.items:
            namespace = objects.Namespace(obj)
            namespaces[namespace.name] = namespace

        return namespaces

    def get_deployments(self, namespace=None, fields=None, labels=None):
        """Get Deployments from the cluster.

        Args:
            namespace (str): The namespace to get the Deployments from. If not
                specified, it will use the auto-generated test case namespace
                by default.
            fields (dict[str, str]): A dictionary of fields used to restrict
                the returned collection of Deployments to only those which match
                these field selectors. By default, no restricting is done.
            labels (dict[str, str]): A dictionary of labels used to restrict
                the returned collection of Deployments to only those which match
                these label selectors. By default, no restricting is done.

        Returns:
            dict[str, objects.Deployment]: A dictionary where the key is
            the Deployment name and the value is the Deployment itself.
        """
        if namespace is None:
            namespace = self.namespace

        selectors = utils.selector_kwargs(fields, labels)

        deployment_list = client.AppsV1Api().list_namespaced_deployment(
            namespace=namespace,
            **selectors,
        )

        deployments = {}
        for obj in deployment_list.items:
            deployment = objects.Deployment(obj)
            deployments[deployment.name] = deployment

        return deployments

    def get_statefulsets(self, namespace=None, fields=None, labels=None):
        """Get StatefulSets from the cluster.

        Args:
            namespace (str): The namespace to get the StatefulSets from. If not
                specified, it will use the auto-generated test case namespace
                by default.
            fields (dict[str, str]): A dictionary of fields used to restrict
                the returned collection of StatefulSets to only those which
                match these field selectors. By default, no restricting is done.
            labels (dict[str, str]): A dictionary of labels used to restrict
                the returned collection of StatefulSets to only those which
                match these label selectors. By default, no restricting is done.

        Returns:
            dict[str, objects.StatefulSet]: A dictionary where the key is
            the StatefulSet name and the value is the StatefulSet itself.
        """
        if namespace is None:
            namespace = self.namespace

        selectors = utils.selector_kwargs(fields, labels)

        statefulset_list = client.AppsV1Api().list_namespaced_stateful_set(
            namespace=namespace,
            **selectors,
        )

        statefulsets = {}
        for obj in statefulset_list.items:
            statefulset = objects.StatefulSet(obj)
            statefulsets[statefulset.name] = statefulset

        return statefulsets

    def get_daemonsets(self, namespace=None, fields=None, labels=None):
        """Get DaemonSets from the cluster.

        Args:
            namespace (str): The namespace to get the DaemonSets from. If not
                specified, it will use the auto-generated test case namespace
                by default.
            fields (dict[str, str]): A dictionary of fields used to restrict
                the returned collection of DaemonSets to only those which
                match these field selectors. By default, no restricting is done.
            labels (dict[str, str]): A dictionary of labels used to restrict
                the returned collection of DaemonSets to only those which
                match these label selectors. By default, no restricting is done.

        Returns:
            dict[str, objects.DaemonSet]: A dictionary where the key is
            the DaemonSet name and the value is the DaemonSet itself.
        """
        if namespace is None:
            namespace = self.namespace

        selectors = utils.selector_kwargs(fields, labels)

        daemonset_list = client.AppsV1Api().list_namespaced_daemon_set(
            namespace=namespace,
            **selectors,
        )

        daemonsets = {}
        for obj in daemonset_list.items:
            daemonset = objects.DaemonSet(obj)
            daemonsets[daemonset.name] = daemonset

        return daemonsets

    def get_endpoints(self, namespace=None, fields=None, labels=None):
        """Get Endpoints from the cluster.

        Args:
            namespace (str): The namespace to get the Endpoints from. If not
                specified, it will use the auto-generated test case namespace
                by default.
            fields (dict[str, str]): A dictionary of fields used to restrict
                the returned collection of Endpoints to only those which match
                these field selectors. By default, no restricting is done.
            labels (dict[str, str]): A dictionary of labels used to restrict
                the returned collection of Endpoints to only those which match
                these label selectors. By default, no restricting is done.

        Returns:
            dict[str, objects.Endpoints]: A dictionary where the key is
            the Endpoint name and the value is the Endpoint itself.
        """
        if namespace is None:
            namespace = self.namespace

        selectors = utils.selector_kwargs(fields, labels)

        endpoints_list = client.CoreV1Api().list_namespaced_endpoints(
            namespace=namespace,
            **selectors,
        )

        endpoints = {}
        for obj in endpoints_list.items:
            endpoint = objects.Endpoints(obj)
            endpoints[endpoint.name] = endpoint

        return endpoints

    def get_secrets(self, namespace=None, fields=None, labels=None):
        """Get Secrets from the cluster.

        Args:
            namespace (str): The namespace to get the Secrets from. If not
                specified, it will use the auto-generated test case namespace
                by default.
            fields (dict[str, str]): A dictionary of fields used to restrict
                the returned collection of Secrets to only those which match
                these field selectors. By default, no restricting is done.
            labels (dict[str, str]): A dictionary of labels used to restrict
                the returned collection of Secrets to only those which match
                these label selectors. By default, no restricting is done.

        Returns:
            dict[str, objects.Secret]: A dictionary where the key is
            the Secret name and the value is the Secret itself.
        """
        if namespace is None:
            namespace = self.namespace

        selectors = utils.selector_kwargs(fields, labels)

        secret_list = client.CoreV1Api().list_namespaced_secret(
            namespace=namespace,
            **selectors,
        )

        secrets = {}
        for obj in secret_list.items:
            secret = objects.Secret(obj)
            secrets[secret.name] = secret

        return secrets

    def get_configmaps(self, namespace=None, fields=None, labels=None):
        """Get ConfigMaps from the cluster.

        Args:
            namespace (str): The namespace to get the ConfigMaps from. If not
                specified, it will use the auto-generated test case namespace
                by default.
            fields (dict[str, str]): A dictionary of fields used to restrict
                the returned collection of ConfigMaps to only those which match
                these field selectors. By default, no restricting is done.
            labels (dict[str, str]): A dictionary of labels used to restrict
                the returned collection of ConfigMaps to only those which match
                these label selectors. By default, no restricting is done.

        Returns:
            dict[str, objects.ConfigMap]: A dictionary where the key is the
            ConfigMap name and the value is the ConfigMap itself.
        """
        if namespace is None:
            namespace = self.namespace

        selectors = utils.selector_kwargs(fields, labels)

        configmap_list = client.CoreV1Api().list_namespaced_config_map(
            namespace=namespace,
            **selectors,
        )

        configmaps = {}
        for obj in configmap_list.items:
            cm = objects.ConfigMap(obj)
            configmaps[cm.name] = cm

        return configmaps

    def get_pods(self, namespace=None, fields=None, labels=None):
        """Get Pods from the cluster.

        Args:
            namespace (str): The namespace to get the Pods from. If not
                specified, it will use the auto-generated test case namespace
                by default.
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
        if namespace is None:
            namespace = self.namespace

        selectors = utils.selector_kwargs(fields, labels)

        pod_list = client.CoreV1Api().list_namespaced_pod(
            namespace=namespace,
            **selectors,
        )

        pods = {}
        for obj in pod_list.items:
            pod = objects.Pod(obj)
            pods[pod.name] = pod

        return pods

    def get_services(self, namespace=None, fields=None, labels=None):
        """Get Services under the test case namespace.

        Args:
            namespace (str): The namespace to get the Services from. If not
                specified, it will use the auto-generated test case namespace
                by default.
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
        if namespace is None:
            namespace = self.namespace

        selectors = utils.selector_kwargs(fields, labels)

        service_list = client.CoreV1Api().list_namespaced_service(
            namespace=namespace,
            **selectors,
        )

        services = {}
        for obj in service_list.items:
            service = objects.Service(obj)
            services[service.name] = service

        return services

    def get_persistentvolume(self, fields=None, labels=None):
        """Get PersistentVolume from the cluster.

        Args:
            fields (dict[str, str]): A dictionary of fields used to restrict
                the returned collection of PersistentVolume to only those which match
                these field selectors. By default, no restricting is done.
            labels (dict[str, str]): A dictionary of labels used to restrict
                the returned collection of PersistentVolume to only those which match
                these label selectors. By default, no restricting is done.

        Returns:
            dict[str, objects.PersistentVolume]: A dictionary where the key is
            the PersistentVolume name and the value is the PersistentVolume itself.
        """
        selectors = utils.selector_kwargs(fields, labels)

        persistentvolume_list = client.CoreV1Api().list_persistent_volume(
                **selectors
        )

        persistentvolumes = {}
        for obj in persistentvolume_list.items:
            persistentvolume = objects.PersistentVolume(obj)
            persistentvolumes[persistentvolume.name] = persistentvolume

        return persistentvolumes

    def get_persistentvolumeclaim(self, namespace=None, fields=None, labels=None):
        """Get PersistentVolumeClaim from the cluster.

        Args:
            namespace (str): The namespace to get the PersistentVolumeClaim from. If not
                specified, it will use the auto-generated test case namespace
                by default.
            fields (dict[str, str]): A dictionary of fields used to restrict
                the returned collection of PersistentVolumeClaim to only those which match
                these field selectors. By default, no restricting is done.
            labels (dict[str, str]): A dictionary of labels used to restrict
                the returned collection of PersistentVolumeClaim to only those which match
                these label selectors. By default, no restricting is done.

        Returns:
            dict[str, objects.PersistentVolumeClaim]: A dictionary where the key is
            the PersistentVolumeClaim name and the value is the PersistentVolumeClaim
            itself.
        """
        if namespace is None:
            namespace = self.namespace

        selectors = utils.selector_kwargs(fields, labels)

        persistentvolumeclaim_list = client.CoreV1Api().\
            list_namespaced_persistent_volume_claim(
            namespace=namespace,
            **selectors,
        )

        persistentvolumeclaims = {}
        for obj in persistentvolumeclaim_list.items:
            persistentvolumeclaim = objects.PersistentVolumeClaim(obj)
            persistentvolumeclaims[persistentvolumeclaim.name] = persistentvolumeclaim

        return persistentvolumeclaims

    @staticmethod
    def get_nodes(fields=None, labels=None):
        """Get the Nodes that make up the cluster.

        Args:
            fields (dict[str, str]): A dictionary of fields used to restrict
                the returned collection of Nodes to only those which match
                these field selectors. By default, no restricting is done.
            labels (dict[str, str]): A dictionary of labels used to restrict
                the returned collection of Nodes to only those which match
                these label selectors. By default, no restricting is done.

        Returns:
            dict[str, objects.Node]: A dictionary where the key is the Node
            name and the value is the Node itself.
        """
        selectors = utils.selector_kwargs(fields, labels)

        node_list = client.CoreV1Api().list_node(
            **selectors,
        )

        nodes = {}
        for obj in node_list.items:
            node = objects.Node(obj)
            nodes[node.name] = node

        return nodes

    def get_events(self, fields=None, labels=None, all_namespaces=False):
        """Get the latest Events that occurred in the cluster.

        Args:
            fields (dict[str, str]): A dictionary of fields used to restrict
                the returned collection of Events to only those which match
                these field selectors. By default, no restricting is done.
            labels (dict[str, str]): A dictionary of labels used to restrict
                the returned collection of Events to only those which match
                these label selectors. By default, no restricting is done.
            all_namespaces (bool): If True, get the events across all
                namespaces.

        Returns:
            dict[str, objects.Event]: A dictionary where the key is the Event
            name and the value is the Event itself.
        """
        selectors = utils.selector_kwargs(fields, labels)

        if all_namespaces:
            event_list = client.CoreV1Api().list_event_for_all_namespaces(
                **selectors
            )
        else:
            event_list = client.CoreV1Api().list_namespaced_event(
                namespace=self.namespace,
                **selectors
            )

        events = {}
        for obj in event_list.items:
            event = objects.Event(obj)
            events[event.name] = event

        return events

    # ****** Test Helpers ******

    @staticmethod
    def wait_for_conditions(
            *args, timeout=None, interval=1, policy=Policy.ONCE, fail_on_api_error=True
    ):
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
            fail_on_api_error (bool): Fail the condition checks if a Kubernetes
                API error is incurred. An API error can be raised for a number
                of reasons, including a Pod being restarted and temporarily
                unavailable. Disabling this will cause those errors to be
                ignored, allowing the check to continue until timeout or
                resolution. (default: True).

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
            'wait for conditions',
            condition_checker,
            to_check,
        )

        try:
            utils.wait_for_condition(
                condition=wait_condition,
                timeout=timeout,
                interval=interval,
                fail_on_api_error=fail_on_api_error,
            )
        except TimeoutError:
            # If we time out here, we want to show all the conditions
            # that we weren't able to resolve in the error message, not
            # the 'wait for conditions' wrapper.
            raise TimeoutError(
                'timed out wile waiting for conditions to be met: {}'.format(to_check)
            )

    def wait_for_ready_nodes(self, count, timeout=None, interval=1):
        """Wait until there are at least ``count`` number of nodes available
        in the cluster.

        Notes:
            This should only be used for clusters that auto-scale the
            nodes. This will not create/delete nodes on its own.

        Args:
            count (int): The number of nodes to wait for.
            timeout (int): The maximum time to wait, in seconds.
            interval (int|float): The time, in seconds, to sleep before
                re-checking the number of nodes.
        """
        def node_count_match(node_count):
            nodes = self.get_nodes()
            return [n.is_ready() for n in nodes.values()].count(True) >= node_count

        wait_condition = Condition(
            'wait for {} nodes'.format(count),
            node_count_match,
            count,
        )

        utils.wait_for_condition(
            condition=wait_condition,
            timeout=timeout,
            interval=interval,
        )

    def wait_for_registered(self, timeout=None, interval=1):
        """Wait for all of the pre-registered objects to be ready on the cluster.

        An object is pre-registered with the test client if it is specified
        to the test via the ``applymanifests`` pytest marker. The marker will load
        the manifest and add the object to the cluster, and register it with
        the test client. This method waits until all such loaded manifest objects
        are in the ready state simultaneously.

        Args:
            timeout (int): The maximum time to wait, in seconds.
            interval (int|float): The time, in seconds, to sleep before
                re-checking the ready state for pre-registered objects.
        """
        def check_registered():
            for obj in self.pre_registered:
                if not obj.is_ready():
                    return False
            return True

        wait_condition = Condition(
            'wait for pre-registered objects to be ready',
            check_registered,
        )

        utils.wait_for_condition(
            condition=wait_condition,
            timeout=timeout,
            interval=interval,
        )

    @staticmethod
    def wait_until_created(obj, timeout=None, interval=1):
        """Wait until the specified object has been created.

        Here, creation is judged on whether or not refreshing the
        object (e.g. getting it) returns an object (created) or
        an error (not yet created).

        Args:
            obj (objects.ApiObject): The ApiObject to wait on.
            timeout (int): The maximum time to wait, in seconds.
            interval (int|float): The time, in seconds, to sleep before
                re-checking the created state of the object.
        """
        def check_ready(api_obj):
            try:
                api_obj.refresh()
            except:  # noqa
                return False
            return True

        wait_condition = Condition(
            'wait for {}:{} to be created'.format(type(obj).__name__, obj.name),
            check_ready,
            obj,
        )

        utils.wait_for_condition(
            condition=wait_condition,
            timeout=timeout,
            interval=interval
        )
