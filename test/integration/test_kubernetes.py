from __future__ import print_function
import json
import os
import time
import unittest

import kubeshift
from kubeshift import validator


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

SIMPLE_POD = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "labels": {
            "app": "sample"
        },
        "name": "sample"
    },
    "spec": {
        "containers": [
            {
                "image": "nginx",
                "name": "sampleworld",
                "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]
            }
        ]
    }
}

PATCH_POD = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "labels": {
            "tier": "webui"
        },
        "name": "sample"
    }
}

REPLACE_POD = {
    "rep": "sampleworldrep"
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

        try:
            self.client.delete(HELLO_B_POD, NAMESPACE)
        except:
            pass

        try:
            self.client.delete(SIMPLE_POD, NAMESPACE)
        except:
            pass

    def test_namespaces(self):
        try:
            self.client.namespaces().all()
        except Exception as err:
            self.fail('namespaces query failed unexpectedly: {}'.format(err))

    def test_create_and_delete(self):
        try:
            self.client.create(HELLO_A_POD, NAMESPACE)
            self.client.delete(HELLO_A_POD, NAMESPACE)
        except Exception as err:
            self.fail('create/delete pod failed unexpectedly: {}'.format(err))

    def test_create_failure(self):
        try:
            self.client.create(HELLO_B_POD, NAMESPACE)
        except Exception as err:
            self.fail('create pod failed unexpectedly: {}'.format(err))

        with self.assertRaises(kubeshift.exceptions.KubeRequestError):
            self.client.create(HELLO_B_POD, NAMESPACE)

    def test_create_replace_modify(self):
        try:
            self.client.create(SIMPLE_POD, NAMESPACE)
            self.client.modify(PATCH_POD, NAMESPACE)

            # give the scheduler a chance to complete the scheduling
            # so that the server side content stablizes otherwise
            # there will be a 409 or 422 related error.
            time.sleep(5)
            apiver, kind, name = validator.validate(SIMPLE_POD)
            url = self.client._generate_url(apiver, kind, NAMESPACE, name)
            obj = self.client.request('get', url)
            print(json.dumps(obj))
            obj['metadata']['labels'].update(REPLACE_POD)
            print(json.dumps(obj))
            self.client.replace(obj, NAMESPACE)
        except Exception as err:
            self.fail('replace/modify pod failed unexpectedly: {}'.format(err))

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
