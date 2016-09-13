import logging
import re
import inspect

from urlparse import urljoin
from urllib import urlencode
from kubeshift.base import KubeBase
from kubeshift.api import Api
from kubeshift.exceptions import KubeKubernetesError

logger = logging.getLogger()


class KubeKubernetesClient(object):

    def __init__(self, config):
        '''

        Args:
            config (obj): Object of the configuration data

        '''

        # The configuration data passed in will be .kube/config data, so process is accordingly.
        self.api = KubeBase(config)

        # Check the API url
        self.base_url = self.api.cluster['server']
        if not re.match('(?:http|https)://', self.base_url):
            raise KubeKubernetesError("Kubernetes API URL does not include HTTP or HTTPS")

        # Gather what end-points we will be using
        self.k8s_api = urljoin(self.base_url, "api/v1/")

        # Test the connection before proceeding
        self.api.test_connection(self.k8s_api)

        # Gather the resource names which will be used for the 'kind' API calls
        self.k8s_api_resources = {}
        self.k8s_api_resources['v1'] = self.api.get_resources(self.k8s_api)

        # Gather what API groups are available
        self.k8s_apis = urljoin(self.base_url, "apis/")

        # Gather the group names from which resource names will be derived
        self.k8s_api_groups = self.api.get_groups(self.k8s_apis)

        # TODO: Needs to be future-proof for v2 API, not just extensions/v1beta1, etc.
        for (name, versions) in self.k8s_api_groups:
            for version in versions:
                api = "%s/%s" % (name, version)
                url = urljoin(self.k8s_apis, api)
                self.k8s_api_resources[api] = self.api.get_resources(url)

    def create(self, obj, namespace):
        '''
        Create an object from the Kubernetes cluster
        '''
        name = KubeBase._get_metadata_name(obj)
        kind, url = self._generate_kurl(obj, namespace)

        self.api.request("post", url, data=obj)

        logger.info("%s '%s' successfully created", kind.capitalize(), name)

    def delete(self, obj, namespace):
        '''
        Delete an object from the Kubernetes cluster

        Args:
            obj (object): Object of the artifact being modified
            namesapce (str): Namespace of the kubernetes cluster to be used
            replicates (int): Default 0, size of the amount of replicas to scale

        *Note*
        Replication controllers must scale to 0 in order to delete pods.
        Kubernetes 1.3 will implement server-side cascading deletion, but
        until then, it's mandatory to scale to 0
        https://github.com/kubernetes/kubernetes/blob/master/docs/proposals/garbage-collection.md

        '''
        name = KubeBase._get_metadata_name(obj)
        kind, url = self._generate_kurl(obj, namespace, name)

        if kind in ['rcs', 'replicationcontrollers']:
            self.scale(obj, namespace)
        self.api.request("delete", url)

        logger.info("%s '%s' successfully deleted", kind.capitalize(), name)

    def scale(self, obj, namespace, replicas=0):
        '''
        By default we scale back down to 0. This function takes an object and scales said
        object down to a specified value on the Kubernetes cluster

        Args:
            obj (object): Object of the artifact being modified
            namesapce (str): Namespace of the kubernetes cluster to be used
            replicates (int): Default 0, size of the amount of replicas to scale
        '''
        patch = [{"op": "replace",
                  "path": "/spec/replicas",
                  "value": replicas}]
        name = KubeBase._get_metadata_name(obj)
        _, url = self._generate_kurl(obj, namespace, name)
        self.api.request("patch", url, data=patch)
        logger.info("'%s' successfully scaled to %s", name, replicas)

    def _generate_kurl(self, obj, namespace, name=None, params=None):
        '''
        Generate the required URL by extracting the 'kind' from the
        object as well as the namespace.

        Args:
            obj (obj): Object of the data being passed
            namespace (str): k8s namespace
            name (str): Name of the object being passed
            params (arr): Extra params passed such as timeout=300

        Returns:
            kind (str): The kind used
            url (str): The URL to be used / artifact URL
        '''
        if 'apiVersion' not in obj.keys():
            raise KubeKubernetesError("Error processing object. There is no apiVersion")

        if 'kind' not in obj.keys():
            raise KubeKubernetesError("Error processing object. There is no kind")

        api_version = obj['apiVersion']

        kind = obj['kind']

        resource = KubeBase.kind_to_resource_name(kind)

        if resource in self.k8s_api_resources[api_version]:
            if api_version == 'v1':
                url = self.k8s_api
            else:
                url = urljoin(self.k8s_apis, "%s/" % api_version)
        else:
            raise KubeKubernetesError("No kind by that name: %s" % kind)

        url = urljoin(url, "namespaces/%s/%s/" % (namespace, resource))

        if name:
            url = urljoin(url, name)

        if params:
            url = urljoin(url, "?%s" % urlencode(params))

        return (resource, url)

    # API CALLS

    # v1

    def bindings(self, namespace):
        return Api(self.api,
                   self.base_url,
                   version="v1",
                   endpoint=inspect.stack()[0][3],
                   namespace=namespace)

    def componentstatuses(self):
        return Api(self.api,
                   self.base_url,
                   version="v1",
                   endpoint=inspect.stack()[0][3])

    def configmaps(self, namespace):
        return Api(self.api,
                   self.base_url,
                   version="v1",
                   endpoint=inspect.stack()[0][3],
                   namespace=namespace)

    def endpoints(self, namespace):
        return Api(self.api,
                   self.base_url,
                   version="v1",
                   endpoint=inspect.stack()[0][3],
                   namespace=namespace)

    def events(self, namespace):
        return Api(self.api,
                   self.base_url,
                   version="v1",
                   endpoint=inspect.stack()[0][3],
                   namespace=namespace)

    def limitranges(self, namespace):
        return Api(self.api,
                   self.base_url,
                   version="v1",
                   endpoint=inspect.stack()[0][3],
                   namespace=namespace)

    def namespaces(self):
        return Api(self.api,
                   self.base_url,
                   version="v1",
                   endpoint=inspect.stack()[0][3])

    def nodes(self):
        return Api(self.api,
                   self.base_url,
                   version="v1",
                   endpoint=inspect.stack()[0][3])

    def persistentvolumeclaims(self, namespace):
        return Api(self.api,
                   self.base_url,
                   version="v1",
                   endpoint=inspect.stack()[0][3],
                   namespace=namespace)

    def persistentvolumes(self):
        return Api(self.api,
                   self.base_url,
                   version="v1",
                   endpoint=inspect.stack()[0][3])

    def pods(self, namespace):
        return Api(self.api,
                   self.base_url,
                   version="v1",
                   endpoint=inspect.stack()[0][3],
                   namespace=namespace)

    def podtemplates(self, namespace):
        return Api(self.api,
                   self.base_url,
                   version="v1",
                   endpoint=inspect.stack()[0][3],
                   namespace=namespace)

    def replicationcontrollers(self, namespace):
        return Api(self.api,
                   self.base_url,
                   version="v1",
                   endpoint=inspect.stack()[0][3],
                   namespace=namespace)

    def resourcequotas(self, namespace):
        return Api(self.api,
                   self.base_url,
                   version="v1",
                   endpoint=inspect.stack()[0][3],
                   namespace=namespace)

    def secrets(self, namespace):
        return Api(self.api,
                   self.base_url,
                   version="v1",
                   endpoint=inspect.stack()[0][3],
                   namespace=namespace)

    def serviceaccounts(self, namespace):
        return Api(self.api,
                   self.base_url,
                   version="v1",
                   endpoint=inspect.stack()[0][3],
                   namespace=namespace)

    def services(self, namespace):
        return Api(self.api,
                   self.base_url,
                   version="v1",
                   endpoint=inspect.stack()[0][3],
                   namespace=namespace)

    # extensions/v1beta1

    def daemonsets(self, namespace):
        return Api(self.api,
                   self.base_url,
                   version="extensions/v1beta1",
                   endpoint=inspect.stack()[0][3],
                   namespace=namespace)

    def deployments(self, namespace):
        return Api(self.api,
                   self.base_url,
                   version="extensions/v1beta1",
                   endpoint=inspect.stack()[0][3],
                   namespace=namespace)

    def horizontalpodautoscalers(self, namespace):
        return Api(self.api,
                   self.base_url,
                   version="extensions/v1beta1",
                   endpoint=inspect.stack()[0][3],
                   namespace=namespace)

    def ingresses(self, namespace):
        return Api(self.api,
                   self.base_url,
                   version="extensions/v1beta1",
                   endpoint=inspect.stack()[0][3],
                   namespace=namespace)

    def jobs(self, namespace):
        return Api(self.api,
                   self.base_url,
                   version="extensions/v1beta1",
                   endpoint=inspect.stack()[0][3],
                   namespace=namespace)

    def networkpolicies(self, namespace):
        return Api(self.api,
                   self.base_url,
                   version="extensions/v1beta1",
                   endpoint=inspect.stack()[0][3],
                   namespace=namespace)

    def replicasets(self, namespace):
        return Api(self.api,
                   self.base_url,
                   version="extensions/v1beta1",
                   endpoint=inspect.stack()[0][3],
                   namespace=namespace)

    def thirdpartyresources(self):
        return Api(self.api,
                   self.base_url,
                   version="extensions/v1beta1",
                   endpoint=inspect.stack()[0][3])

    # apps/v1alpha1

    def petsets(self, namespace):
        return Api(self.api,
                   self.base_url,
                   version="apps/v1alpha1",
                   endpoint=inspect.stack()[0][3],
                   namespace=namespace)

    # policy/v1alpha1

    def poddisruptionbudgets(self, namespace):
        return Api(self.api,
                   self.base_url,
                   version="policy/v1alpha1",
                   endpoint=inspect.stack()[0][3],
                   namespace=namespace)
