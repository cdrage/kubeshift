"""Kubernetes names query APIs."""
from kubeshift.constants import DEFAULT_NAMESPACE
from kubeshift.queries import base


class KubeQueryMixin(object):
    """Provide Kubernetes name query APIs."""

    # v1

    @base.queryapi(version='v1', kind='ComponentStatus', nsarg=False)
    def componentstatuses(self):
        """:py:class:`~kubeshift.queries.base.Query` componentstatuses."""

    @base.queryapi(version='v1', kind='ConfigMap')
    def configmaps(self, namespace=DEFAULT_NAMESPACE):
        """:py:class:`~kubeshift.queries.base.Query` configmaps."""

    @base.queryapi(version='v1', kind='Endpoints')
    def endpoints(self, namespace=DEFAULT_NAMESPACE):
        """:py:class:`~kubeshift.queries.base.Query` endpoints."""

    @base.queryapi(version='v1', kind='Event')
    def events(self, namespace=DEFAULT_NAMESPACE):
        """:py:class:`~kubeshift.queries.base.Query` events."""

    @base.queryapi(version='v1', kind='LimitRange')
    def limitranges(self, namespace=DEFAULT_NAMESPACE):
        """:py:class:`~kubeshift.queries.base.Query` limitranges."""

    @base.queryapi(version='v1', kind='Namespace')
    def namespaces(self):
        """:py:class:`~kubeshift.queries.base.Query` namespaces."""

    @base.queryapi(version='v1', kind='Node', nsarg=False)
    def nodes(self):
        """:py:class:`~kubeshift.queries.base.Query` nodes."""

    @base.queryapi(version='v1', kind='PersistentVolumeClaim')
    def persistentvolumeclaims(self, namespace=DEFAULT_NAMESPACE):
        """:py:class:`~kubeshift.queries.base.Query` persistentvolumeclaims."""

    @base.queryapi(version='v1', kind='PersistentVolume', nsarg=False)
    def persistentvolumes(self):
        """:py:class:`~kubeshift.queries.base.Query` persistentvolumes."""

    @base.queryapi(version='v1', kind='Pod')
    def pods(self, namespace=DEFAULT_NAMESPACE):
        """:py:class:`~kubeshift.queries.base.Query` pods."""

    @base.queryapi(version='v1', kind='PodTemplate')
    def podtemplates(self, namespace=DEFAULT_NAMESPACE):
        """:py:class:`~kubeshift.queries.base.Query` podtemplates."""

    @base.queryapi(version='v1', kind='ReplicationController')
    def replicationcontrollers(self, namespace=DEFAULT_NAMESPACE):
        """:py:class:`~kubeshift.queries.base.Query` replicationcontrollers."""

    @base.queryapi(version='v1', kind='ResourceQuota')
    def resourcequotas(self, namespace=DEFAULT_NAMESPACE):
        """:py:class:`~kubeshift.queries.base.Query` resourcequotas."""

    @base.queryapi(version='v1', kind='Secret')
    def secrets(self, namespace=DEFAULT_NAMESPACE):
        """:py:class:`~kubeshift.queries.base.Query` secrets."""

    @base.queryapi(version='v1', kind='ServiceAccount')
    def serviceaccounts(self, namespace=DEFAULT_NAMESPACE):
        """:py:class:`~kubeshift.queries.base.Query` serviceaccounts."""

    @base.queryapi(version='v1', kind='Service')
    def services(self, namespace=DEFAULT_NAMESPACE):
        """:py:class:`~kubeshift.queries.base.Query` services."""

    # extensions/v1beta1

    @base.queryapi(version='extensions/v1beta1', kind='DaemonSet')
    def daemonsets(self, namespace=DEFAULT_NAMESPACE):
        """:py:class:`~kubeshift.queries.base.Query` daemonsets."""

    @base.queryapi(version='extensions/v1beta1', kind='Deployment')
    def deployments(self, namespace=DEFAULT_NAMESPACE):
        """:py:class:`~kubeshift.queries.base.Query` deployments."""

    @base.queryapi(version='extensions/v1beta1', kind='HorizontalPodAutoscaler')
    def horizontalpodautoscalers(self, namespace=DEFAULT_NAMESPACE):
        """:py:class:`~kubeshift.queries.base.Query` horizontalpodautoscalers."""

    @base.queryapi(version='extensions/v1beta1', kind='Ingress')
    def ingresses(self, namespace=DEFAULT_NAMESPACE):
        """:py:class:`~kubeshift.queries.base.Query` ingresses."""

    @base.queryapi(version='extensions/v1beta1', kind='Job')
    def jobs(self, namespace=DEFAULT_NAMESPACE):
        """:py:class:`~kubeshift.queries.base.Query` jobs."""

    @base.queryapi(version='extensions/v1beta1', kind='NetworkPolicy')
    def networkpolicies(self, namespace=DEFAULT_NAMESPACE):
        """:py:class:`~kubeshift.queries.base.Query` networkpolicies."""

    @base.queryapi(version='extensions/v1beta1', kind='ReplicaSet')
    def replicasets(self, namespace=DEFAULT_NAMESPACE):
        """:py:class:`~kubeshift.queries.base.Query` replicasets."""

    @base.queryapi(version='extensions/v1beta1', kind='ThirdPartyResource', nsarg=False)
    def thirdpartyresources(self):
        """:py:class:`~kubeshift.queries.base.Query` thirdpartyresources."""

    # apps/v1alpha1

    @base.queryapi(version='apps/v1alpha1', kind='PetSet')
    def petsets(self, namespace=DEFAULT_NAMESPACE):
        """:py:class:`~kubeshift.queries.base.Query` petsets."""
