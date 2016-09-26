import os
import unittest

import kubeshift


HELLO_A_POD = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "labels": {
            "app": "hellonginx"
        },
        "name": "hellonginx"
    },
    "spec": {
        "containers": [
            {
                "image": "nginx",
                "name": "hellonginx",
                "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]
            }
        ]
    }
}

HELLO_B_POD = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "labels": {
            "app": "helloworld"
        },
        "name": "helloworld"
    },
    "spec": {
        "containers": [
            {
                "image": "nginx",
                "name": "helloworld",
                "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]
            }
        ]
    }
}

KUBE_CONFIG_FILE = os.getenv('KUBE_CONFIG_FILE')
NAMESPACE = os.getenv('NAMESPACE', 'default')


class TestKubernetes(unittest.TestCase):

    def setUp(self):
        cfg = kubeshift.Config.from_file(KUBE_CONFIG_FILE)
        self.client = kubeshift.KubernetesClient(cfg)

    def tearDown(self):
        try:
            self.client.delete(HELLO_A_POD, NAMESPACE)
        except:
            pass

    def test_namespaces(self):
        self.client.namespaces().all()

    def test_create_and_delete(self):
        self.client.create(HELLO_A_POD, NAMESPACE)
        self.client.delete(HELLO_A_POD, NAMESPACE)

    def test_create_failure(self):
        self.client.create(HELLO_B_POD, NAMESPACE)
        with self.assertRaises(kubeshift.exceptions.KubeRequestError):
            self.client.create(HELLO_B_POD, NAMESPACE)

    def test_api_calls(self):
        apis = [
            'componentstatuses',
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
            'replicationcontrollers',
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
        ]
        for a in apis:
            self.assertIsNotNone(getattr(self.client, a)().all())
