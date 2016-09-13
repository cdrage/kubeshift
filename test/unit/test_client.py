import mock
import pytest
from kubeshift.client import Client
from kubeshift.exceptions import KubeClientError

config = {
    "kind": "Config",
    "preferences": {},
    "current-context": "dev",
    "contexts": [
            {
                "name": "dev",
                "context": {
                    "cluster": "dev",
                    "user": "default"
                }
            }
    ],
    "clusters": [
        {
            "cluster": {
                "server": "http://localhost:8080"
            },
            "name": "dev"
        }
    ],
    "apiVersion": "v1",
    "users": [
        {
            "name": "default",
            "user": {
                    "token": "foobar"
            }
        }
    ]
}


class FakeConfig():

    def __init__(self, *args):
        pass


@mock.patch("kubeshift.client.KubeKubernetesClient")
def test_client_kubernetes(FakeConfig):
    Client(config, "kubernetes")


@mock.patch("kubeshift.client.KubeOpenshiftClient")
def test_client_openshift(FakeConfig):
    Client(config, "openshift")


def test_client_load_failure():
    with pytest.raises(KubeClientError):
        Client(config, "foobar")


class FakeClient():

    def __init__(self, *args):
        pass

    def test_connection(self, *args):
        pass

    def get_resources(self, *args):
        return ['Pod', 'pod', 'pods']

    def get_groups(self, *args):
        return {}

    def request(self, method, url, data=None):
        return None

    @property
    def cluster(self):
        return {'server': 'https://foobar'}


@mock.patch("kubeshift.kubernetes.KubeBase")
def test_client_create_with_kubernetes(mock_class):
    # Mock the API class
    mock_class.return_value = FakeClient()
    mock_class.kind_to_resource_name.return_value = 'Pod'

    k8s_object = {"apiVersion": "v1", "kind": "Pod", "metadata": {"labels": {"app": "helloapache"}, "name": "helloapache"}, "spec": {
        "containers": [{"image": "$image", "name": "helloapache", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}

    Client(config, "kubernetes").create(k8s_object)


@mock.patch("kubeshift.kubernetes.KubeBase")
def test_client_delete_with_kubernetes(mock_class):
    # Mock the API class
    mock_class.return_value = FakeClient()
    mock_class.kind_to_resource_name.return_value = 'Pod'

    k8s_object = {"apiVersion": "v1", "kind": "Pod", "metadata": {"labels": {"app": "helloapache"}, "name": "helloapache"}, "spec": {
        "containers": [{"image": "$image", "name": "helloapache", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}

    Client(config, "kubernetes").delete(k8s_object)


class FakeClientWithNamespaces():

    def __init__(self, *args):
        pass

    def test_connection(self, *args):
        pass

    def get_resources(self, *args):
        return ['Pod', 'pod', 'pods']

    def get_groups(self, *args):
        return {}

    def request(self, method, url, data=None):
        return {'items': [{'metadata': {'name': 'foo'}}]}

    @property
    def cluster(self):
        return {'server': 'https://foobar'}


@mock.patch("kubeshift.kubernetes.KubeBase")
@mock.patch("kubeshift.openshift.KubeBase")
def test_client_api_calls(mock_k8s_class, mock_oc_class):
    mock_k8s_class.return_value = FakeClientWithNamespaces()
    mock_oc_class.return_value = FakeClientWithNamespaces()

    k8s = Client(config, "kubernetes")
    oc = Client(config, "openshift")

    calls = ['componentstatuses',
             'configmaps',
             'endpoints',
             'events',
             'limitranges',
             'namespaces',
             'nodes',
             'persistentvolumeclaims',
             'persistentvolumes',
             'pods',
             'podtemplates',
             'resourcequotas',
             'secrets',
             'serviceaccounts',
             'services',
             'daemonsets',
             'deployments',
             'horizontalpodautoscalers',
             'ingresses',
             'jobs',
             'networkpolicies',
             'replicasets',
             'thirdpartyresources',
             'petsets',
             'poddisruptionbudgets']
    for a in calls:
        getattr(k8s, a)()
        getattr(oc, a)()
