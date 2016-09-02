import unittest
import subprocess
import getpass
import pytest
import kubeshift


class TestKubernetes(unittest.TestCase):

    # Bring the k8s cluster up (only needs to happen once)
    @classmethod
    def setUpClass(cls):
        subprocess.call("./test/integration/providers/kubernetes.sh start", shell=True)
        subprocess.call("./test/integration/providers/kubernetes.sh config", shell=True)

    # Tear down the k8s cluster (only needs to happen once)
    @classmethod
    def tearDownClass(cls):
        subprocess.call("./test/integration/providers/kubernetes.sh clean", shell=True)
        subprocess.call("./test/integration/providers/kubernetes.sh wait", shell=True)
        subprocess.call("./test/integration/providers/kubernetes.sh stop", shell=True)

    # Setup the client on each function run
    def setUp(self):
        user = getpass.getuser()
        self.client = kubeshift.Client(kubeshift.Config.from_file("/home/%s/.kube/config" % user), "kubernetes")

    # Clean the cluster on each function run
    def tearDown(self):
        subprocess.call("./test/integration/providers/kubernetes.sh clean", shell=True)
        subprocess.call("./test/integration/providers/kubernetes.sh wait", shell=True)

    def test_namespaces(self):
        assert self.client.namespaces() == ['default', 'kube-system']

    def test_create_and_delete(self):
        k8s_object = {"apiVersion": "v1", "kind": "Pod", "metadata": {"labels": {"app": "hellonginx"}, "name": "hellonginx"}, "spec": {"containers": [{"image": "nginx", "name": "hellonginx", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}
        self.client.create(k8s_object)
        self.client.delete(k8s_object)

    def test_create_failure(self):
        k8s_object = {"apiVersion": "v1", "kind": "Pod", "metadata": {"labels": {"app": "hellonginx"}, "name": "hellonginx"}, "spec": {"containers": [{"image": "nginx", "name": "hellonginx", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}
        self.client.create(k8s_object)
        with pytest.raises(kubeshift.exceptions.KubeConnectionError):
            self.client.create(k8s_object)
