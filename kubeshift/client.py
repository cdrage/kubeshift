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

    # Current support: kubernetes only
    def namespaces(self):
        return self.connection.namespaces()
