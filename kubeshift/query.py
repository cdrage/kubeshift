"""Perform API query for any provider with filtering features."""
import six

from kubeshift.constants import DEFAULT_NAMESPACE


class Query(object):
    """Performs queries with filters."""

    def __init__(self, client, url):
        """
        Use a Provider client and lookup for specific API..

        client [KubeBase]
        """
        self.client = client
        self.url = url

    def all(self):
        """Perform query with no filters (all results)."""
        return self.client.request("get", self.url) or {}

    def items(self):
        """Select the list of items from the query results."""
        return self.all().get('items', [])

    def metadata(self):
        """Filter the results to provide only the metadata only."""
        return [s.get('metadata', {}) for s in self.items()]

    def filter(self, namespace=None, status=None):
        """
        Filter by namespace and/or status.

        Apply one or both filter(s) provided to the query results.
        """
        if namespace and status:
            return [s for s in self.items() if s.get('metadata', {}).get('namespace') == namespace and s.get('status', {}).get('phase') == status]
        elif namespace:
            return [s for s in self.items() if s.get('metadata', {}).get('namespace') == namespace]
        elif status:
            return [s for s in self.items() if s.get('status', {}).get('phase') == status]

        return []


def queryapi(version, kind, nsarg=True):
    """Make Query API.

    .. py:decorator:: queryapi

        Creates a named query api.
    """
    def decorator(func):
        @six.wraps(func)
        def handler(self, namespace=DEFAULT_NAMESPACE):
            if not nsarg:
                namespace = None
            url = self._generate_url(api_version=version,
                                     kind=kind,
                                     namespace=namespace)
            return Query(self, url)
        return handler
    return decorator


class QueryMixin(object):
    """Provide named Query APIs."""

    # v1

    @queryapi(version='v1', kind='ComponentStatus', nsarg=False)
    def componentstatuses(self):
        """Query componentstatuses."""

    @queryapi(version='v1', kind='ConfigMap')
    def configmaps(self, namespace=DEFAULT_NAMESPACE):
        """Query configmaps."""

    @queryapi(version='v1', kind='Endpoints')
    def endpoints(self, namespace=DEFAULT_NAMESPACE):
        """Query endpoints."""

    @queryapi(version='v1', kind='Event')
    def events(self, namespace=DEFAULT_NAMESPACE):
        """Query events."""

    @queryapi(version='v1', kind='LimitRange')
    def limitranges(self, namespace=DEFAULT_NAMESPACE):
        """Query limitranges."""

    @queryapi(version='v1', kind='Namespace')
    def namespaces(self):
        """Query namespaces."""

    @queryapi(version='v1', kind='Node', nsarg=False)
    def nodes(self):
        """Query nodes."""

    @queryapi(version='v1', kind='PersistentVolumeClaim')
    def persistentvolumeclaims(self, namespace=DEFAULT_NAMESPACE):
        """Query persistentvolumeclaims."""

    @queryapi(version='v1', kind='PersistentVolume', nsarg=False)
    def persistentvolumes(self):
        """Query persistentvolumes."""

    @queryapi(version='v1', kind='Pod')
    def pods(self, namespace=DEFAULT_NAMESPACE):
        """Query pods."""

    @queryapi(version='v1', kind='PodTemplate')
    def podtemplates(self, namespace=DEFAULT_NAMESPACE):
        """Query podtemplates."""

    @queryapi(version='v1', kind='ReplicationController')
    def replicationcontrollers(self, namespace=DEFAULT_NAMESPACE):
        """Query replicationcontrollers."""

    @queryapi(version='v1', kind='ResourceQuota')
    def resourcequotas(self, namespace=DEFAULT_NAMESPACE):
        """Query resourcequotas."""

    @queryapi(version='v1', kind='Secret')
    def secrets(self, namespace=DEFAULT_NAMESPACE):
        """Query secrets."""

    @queryapi(version='v1', kind='ServiceAccount')
    def serviceaccounts(self, namespace=DEFAULT_NAMESPACE):
        """Query serviceaccounts."""

    @queryapi(version='v1', kind='Service')
    def services(self, namespace=DEFAULT_NAMESPACE):
        """Query services."""

    # extensions/v1beta1

    @queryapi(version='extensions/v1beta1', kind='DaemonSet')
    def daemonsets(self, namespace=DEFAULT_NAMESPACE):
        """Query daemonsets."""

    @queryapi(version='extensions/v1beta1', kind='Deployment')
    def deployments(self, namespace=DEFAULT_NAMESPACE):
        """Query deployments."""

    @queryapi(version='extensions/v1beta1', kind='HorizontalPodAutoscaler')
    def horizontalpodautoscalers(self, namespace=DEFAULT_NAMESPACE):
        """Query horizontalpodautoscalers."""

    @queryapi(version='extensions/v1beta1', kind='Ingress')
    def ingresses(self, namespace=DEFAULT_NAMESPACE):
        """Query ingresses."""

    @queryapi(version='extensions/v1beta1', kind='Job')
    def jobs(self, namespace=DEFAULT_NAMESPACE):
        """Query jobs."""

    @queryapi(version='extensions/v1beta1', kind='NetworkPolicy')
    def networkpolicies(self, namespace=DEFAULT_NAMESPACE):
        """Query networkpolicies."""

    @queryapi(version='extensions/v1beta1', kind='ReplicaSet')
    def replicasets(self, namespace=DEFAULT_NAMESPACE):
        """Query replicasets."""

    @queryapi(version='extensions/v1beta1', kind='ThirdPartyResource', nsarg=False)
    def thirdpartyresources(self):
        """Query thirdpartyresources."""

    # apps/v1alpha1

    @queryapi(version='apps/v1alpha1', kind='PetSet')
    def petsets(self, namespace=DEFAULT_NAMESPACE):
        """Query petsets."""
