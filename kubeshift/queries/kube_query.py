"""Kubernetes names query APIs."""
from kubeshift.constants import DEFAULT_NAMESPACE
from kubeshift.queries import base


class KubeQueryMixin(object):
    """Provide Kubernetes name query APIs."""

    # v1

    @base.queryapi(version='v1', kind='ComponentStatus', nsarg=False)
    def componentstatuses(self):
        """Query componentstatuses."""

    @base.queryapi(version='v1', kind='ConfigMap')
    def configmaps(self, namespace=DEFAULT_NAMESPACE):
        """Query configmaps."""

    @base.queryapi(version='v1', kind='Endpoints')
    def endpoints(self, namespace=DEFAULT_NAMESPACE):
        """Query endpoints."""

    @base.queryapi(version='v1', kind='Event')
    def events(self, namespace=DEFAULT_NAMESPACE):
        """Query events."""

    @base.queryapi(version='v1', kind='LimitRange')
    def limitranges(self, namespace=DEFAULT_NAMESPACE):
        """Query limitranges."""

    @base.queryapi(version='v1', kind='Namespace')
    def namespaces(self):
        """Query namespaces."""

    @base.queryapi(version='v1', kind='Node', nsarg=False)
    def nodes(self):
        """Query nodes."""

    @base.queryapi(version='v1', kind='PersistentVolumeClaim')
    def persistentvolumeclaims(self, namespace=DEFAULT_NAMESPACE):
        """Query persistentvolumeclaims."""

    @base.queryapi(version='v1', kind='PersistentVolume', nsarg=False)
    def persistentvolumes(self):
        """Query persistentvolumes."""

    @base.queryapi(version='v1', kind='Pod')
    def pods(self, namespace=DEFAULT_NAMESPACE):
        """Query pods."""

    @base.queryapi(version='v1', kind='PodTemplate')
    def podtemplates(self, namespace=DEFAULT_NAMESPACE):
        """Query podtemplates."""

    @base.queryapi(version='v1', kind='ReplicationController')
    def replicationcontrollers(self, namespace=DEFAULT_NAMESPACE):
        """Query replicationcontrollers."""

    @base.queryapi(version='v1', kind='ResourceQuota')
    def resourcequotas(self, namespace=DEFAULT_NAMESPACE):
        """Query resourcequotas."""

    @base.queryapi(version='v1', kind='Secret')
    def secrets(self, namespace=DEFAULT_NAMESPACE):
        """Query secrets."""

    @base.queryapi(version='v1', kind='ServiceAccount')
    def serviceaccounts(self, namespace=DEFAULT_NAMESPACE):
        """Query serviceaccounts."""

    @base.queryapi(version='v1', kind='Service')
    def services(self, namespace=DEFAULT_NAMESPACE):
        """Query services."""

    # extensions/v1beta1

    @base.queryapi(version='extensions/v1beta1', kind='DaemonSet')
    def daemonsets(self, namespace=DEFAULT_NAMESPACE):
        """Query daemonsets."""

    @base.queryapi(version='extensions/v1beta1', kind='Deployment')
    def deployments(self, namespace=DEFAULT_NAMESPACE):
        """Query deployments."""

    @base.queryapi(version='extensions/v1beta1', kind='HorizontalPodAutoscaler')
    def horizontalpodautoscalers(self, namespace=DEFAULT_NAMESPACE):
        """Query horizontalpodautoscalers."""

    @base.queryapi(version='extensions/v1beta1', kind='Ingress')
    def ingresses(self, namespace=DEFAULT_NAMESPACE):
        """Query ingresses."""

    @base.queryapi(version='extensions/v1beta1', kind='Job')
    def jobs(self, namespace=DEFAULT_NAMESPACE):
        """Query jobs."""

    @base.queryapi(version='extensions/v1beta1', kind='NetworkPolicy')
    def networkpolicies(self, namespace=DEFAULT_NAMESPACE):
        """Query networkpolicies."""

    @base.queryapi(version='extensions/v1beta1', kind='ReplicaSet')
    def replicasets(self, namespace=DEFAULT_NAMESPACE):
        """Query replicasets."""

    @base.queryapi(version='extensions/v1beta1', kind='ThirdPartyResource', nsarg=False)
    def thirdpartyresources(self):
        """Query thirdpartyresources."""

    # apps/v1alpha1

    @base.queryapi(version='apps/v1alpha1', kind='PetSet')
    def petsets(self, namespace=DEFAULT_NAMESPACE):
        """Query petsets."""
