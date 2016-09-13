from kubeshift.kubernetes import KubeKubernetesClient
from kubeshift.openshift import KubeOpenshiftClient
from kubeshift.exceptions import KubeClientError
import logging

logger = logging.getLogger()


class Client(object):

    def __init__(self, config, provider):
        '''

        Args:
            config (obj): Object of the configuration data
            provider (str): String value of the provider that is being used

        '''
        self.config = config
        self.provider = provider

        # Choose the type of provider that is being used. Error out if it is not available
        if provider is "kubernetes":
            self.connection = KubeKubernetesClient(config)
            logger.debug("Using Kubernetes Provider KubeClient library")
        elif provider is "openshift":
            self.connection = KubeOpenshiftClient(config)
            logger.debug("Using OpenShift Provider KubeClient library")
        else:
            raise KubeClientError("No provider by that name.")

    # Create an object using its respective API
    def create(self, obj, namespace="default"):
        self.connection.create(obj, namespace)

    # Delete an object using its respective API
    def delete(self, obj, namespace="default"):
        self.connection.delete(obj, namespace)

    # Scale an object using its respective API
    def scale(self, obj, namespace="default", replicas=0):
        self.connection.scale(obj, namespace, namespace, replicas)

    # API calls

    # v1

    def componentstatuses(self):
        return self.connection.componentstatuses()

    def configmaps(self, namespace="default"):
        return self.connection.configmaps(namespace)

    def endpoints(self, namespace="default"):
        return self.connection.endpoints(namespace)

    def events(self, namespace="default"):
        return self.connection.events(namespace)

    def limitranges(self, namespace="default"):
        return self.connection.limitranges(namespace)

    def namespaces(self):
        return self.connection.namespaces()

    def nodes(self):
        return self.connection.nodes()

    def persistentvolumeclaims(self, namespace="default"):
        return self.connection.persistentvolumeclaims(namespace)

    def persistentvolumes(self):
        return self.connection.persistentvolumes()

    def pods(self, namespace="default"):
        return self.connection.pods(namespace)

    def podtemplates(self, namespace="default"):
        return self.connection.podtemplates(namespace)

    def replicationcontrollers(self, namespace="default"):
        return self.connection.replicationcontrollers(namespace)

    def resourcequotas(self, namespace="default"):
        return self.connection.resourcequotas(namespace)

    def secrets(self, namespace="default"):
        return self.connection.secrets(namespace)

    def serviceaccounts(self, namespace="default"):
        return self.connection.serviceaccounts(namespace)

    def services(self, namespace="default"):
        return self.connection.services(namespace)

    # extensions/v1beta1

    def daemonsets(self, namespace="default"):
        return self.connection.daemonsets(namespace)

    def deployments(self, namespace="default"):
        return self.connection.deployments(namespace)

    def horizontalpodautoscalers(self, namespace="default"):
        return self.connection.horizontalpodautoscalers(namespace)

    def ingresses(self, namespace="default"):
        return self.connection.ingresses(namespace)

    def jobs(self, namespace="default"):
        return self.connection.jobs(namespace)

    def networkpolicies(self, namespace="default"):
        return self.connection.networkpolicies(namespace)

    def replicasets(self, namespace="default"):
        return self.connection.replicasets(namespace)

    def thirdpartyresources(self):
        return self.connection.thirdpartyresources()

    # apps/v1alpha1

    def petsets(self, namespace="default"):
        return self.connection.petsets(namespace)

    # policy/v1alpha1

    def poddisruptionbudgets(self, namespace="default"):
        return self.connection.poddisruptionbudgets(namespace)
