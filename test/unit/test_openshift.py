import mock
import pytest
from copy import deepcopy
from kubeshift.openshift import KubeOpenshiftClient
from kubeshift.exceptions import KubeOpenshiftError, KubeBaseError

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


class FakeClient():

    def __init__(self, *args):
        pass

    def test_connection(self, *args):
        pass

    def get_resources(self, *args):
        return ['Pod', 'template']

    def get_groups(self, *args):
        return {}

    def request(self, method, url, data=None):
        return None, 200

    @property
    def cluster(self):
        return {'server': 'https://foobar'}


@mock.patch("kubeshift.openshift.KubeBase")
def test_create(mock_class):
    # Mock the API class
    mock_class.return_value = FakeClient()
    mock_class.get_resources.return_value = ['Pod']
    mock_class.kind_to_resource_name.return_value = 'Pod'

    k8s_object = {"apiVersion": "v1", "kind": "Pod", "metadata": {"labels": {"app": "helloapache"}, "name": "helloapache"}, "spec": {
        "containers": [{"image": "$image", "name": "helloapache", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}

    a = KubeOpenshiftClient(config)
    a.create(k8s_object, "foobar")


@mock.patch("kubeshift.openshift.KubeBase")
def test_delete(mock_class):
    # Mock the API class
    mock_class.return_value = FakeClient()
    mock_class.kind_to_resource_name.return_value = 'Pod'

    k8s_object = {"apiVersion": "v1", "kind": "Pod", "metadata": {"labels": {"app": "helloapache"}, "name": "helloapache"}, "spec": {
        "containers": [{"image": "$image", "name": "helloapache", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}

    a = KubeOpenshiftClient(config)
    a.delete(k8s_object, "foobar")


class FakeOpenshiftTemplateClient():

    def __init__(self, *args):
        pass

    def test_connection(self, *args):
        pass

    def get_resources(self, *args):
        return ['Pod', 'template']

    def get_groups(self, *args):
        return {}

    def request(self, method, url, data=None):
        openshift_object = {}
        openshift_object['objects'] = [{"kind": "Service", "apiVersion": "v1", "metadata": {"name": "cakephp-mysql-example", "annotations": {
            "description": "Exposes and load balances the application pods"}}, "spec": {"ports": [{"name": "web", "port": 8080, "targetPort": 8080}], "selector": {"name": "cakephp-mysql-example"}}}]
        return openshift_object, 200

    @property
    def cluster(self):
        return {'server': 'https://foobar'}


@mock.patch("kubeshift.openshift.KubeBase")
def test_process_template(mock_class):
    # Mock the API class
    mock_class.return_value = FakeOpenshiftTemplateClient()
    mock_class.kind_to_resource_name.return_value = 'template'

    openshift_template = {"kind": "Template", "apiVersion": "v1", "metadata": {"name": "foobar"}, "objects": [{"kind": "Service", "apiVersion": "v1", "metadata": {"name": "cakephp-mysql-example", "annotations": {
        "description": "Exposes and load balances the application pods"}}, "spec": {"ports": [{"name": "web", "port": 8080, "targetPort": 8080}], "selector": {"name": "cakephp-mysql-example"}}}]}

    a = KubeOpenshiftClient(config)
    a.create(openshift_template, "foobar")
    a.delete(openshift_template, "foobar")


def test_init_non_http():
    mod_config = deepcopy(config)
    mod_config['clusters'][0]['cluster']['server'] = "foo"
    with pytest.raises(KubeOpenshiftError):
        KubeOpenshiftClient(mod_config)


def test_connection(*args):
    pass


def get_resources(*args):
    return ['Pod', 'pod', 'pods']


def get_groups(*args):
    return {}


def get_groups_example(*args):
    data = {"kind": "APIGroupList", "groups": [{"name": "autoscaling", "versions": [{"groupVersion": "autoscaling/v1", "version": "v1"}], "preferredVersion": {"groupVersion": "autoscaling/v1", "version": "v1"}, "serverAddressByClientCIDRs": [{"clientCIDR": "0.0.0.0/0", "serverAddress": "192.168.1.156:443"}]}, {"name": "batch", "versions": [{"groupVersion": "batch/v1", "version": "v1"}], "preferredVersion": {
        "groupVersion": "batch/v1", "version": "v1"}, "serverAddressByClientCIDRs": [{"clientCIDR": "0.0.0.0/0", "serverAddress": "192.168.1.156:443"}]}, {"name": "extensions", "versions": [{"groupVersion": "extensions/v1beta1", "version": "v1beta1"}], "preferredVersion": {"groupVersion": "extensions/v1beta1", "version": "v1beta1"}, "serverAddressByClientCIDRs": [{"clientCIDR": "0.0.0.0/0", "serverAddress": "192.168.1.156:443"}]}]}
    groups = data["groups"] or []
    groups = [(group['name'], [i['version'] for i in group['versions']]) for group in groups]
    return groups


def request(method, url, data=None):
    return None, 200


@mock.patch("kubeshift.openshift.KubeBase.test_connection", side_effect=test_connection)
@mock.patch("kubeshift.openshift.KubeBase.get_resources", side_effect=get_resources)
@mock.patch("kubeshift.openshift.KubeBase.get_groups", side_effect=get_groups_example)
def test_init_with_groups(utest_connection, uget_resources, uget_groups):
    KubeOpenshiftClient(config)


@mock.patch("kubeshift.openshift.KubeBase.test_connection", side_effect=test_connection)
@mock.patch("kubeshift.openshift.KubeBase.get_resources", return_value=['replicationcontrollers'])
@mock.patch("kubeshift.openshift.KubeBase.get_groups", side_effect=get_groups)
@mock.patch("kubeshift.openshift.KubeBase.request", side_effect=request)
@mock.patch("kubeshift.openshift.KubeBase.kind_to_resource_name", return_value='replicationcontrollers')
def test_scale(utest_connection, uget_resources, uget_groups, urequest, ukind_to_resource_name):
    # Mock the API class
    k8s_object = {"apiVersion": "v1", "kind": "ReplicationController", "metadata": {"labels": {"app": "helloapache"}, "name": "helloapache"}, "spec": {
        "containers": [{"image": "$image", "name": "helloapache", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}

    a = KubeOpenshiftClient(config)
    a.scale(k8s_object, "foobar")


@mock.patch("kubeshift.openshift.KubeBase.test_connection", side_effect=test_connection)
@mock.patch("kubeshift.openshift.KubeBase.get_resources", side_effect=get_resources)
@mock.patch("kubeshift.openshift.KubeBase.get_groups", side_effect=get_groups)
@mock.patch("kubeshift.openshift.KubeBase.request", side_effect=request)
@mock.patch("kubeshift.openshift.KubeBase.kind_to_resource_name", return_value='Pod')
def test_create_without_api_version(utest_connection, uget_resources, uget_groups, urequest, ukind_to_resource_name):
    # Mock the API class
    k8s_object = {"kind": "Pod", "metadata": {"labels": {"app": "helloapache"}, "name": "helloapache"}, "spec": {
        "containers": [{"image": "$image", "name": "helloapache", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}

    a = KubeOpenshiftClient(config)

    with pytest.raises(KubeOpenshiftError):
        a.create(k8s_object, "foobar")


@mock.patch("kubeshift.openshift.KubeBase.test_connection", side_effect=test_connection)
@mock.patch("kubeshift.openshift.KubeBase.get_resources", side_effect=get_resources)
@mock.patch("kubeshift.openshift.KubeBase.get_groups", side_effect=get_groups_example)
@mock.patch("kubeshift.openshift.KubeBase.request", side_effect=request)
@mock.patch("kubeshift.openshift.KubeBase.kind_to_resource_name", return_value='Pod')
def test_create_with_v1beta1(utest_connection, uget_resources, uget_groups, urequest, ukind_to_resource_name):
    # Mock the API class
    k8s_object = {"apiVersion": "extensions/v1beta1", "kind": "Pod", "metadata": {"labels": {"app": "helloapache"}, "name": "helloapache"}, "spec": {
        "containers": [{"image": "$image", "name": "helloapache", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}

    a = KubeOpenshiftClient(config)

    a.create(k8s_object, "foobar")


@mock.patch("kubeshift.openshift.KubeBase.test_connection", side_effect=test_connection)
@mock.patch("kubeshift.openshift.KubeBase.get_resources", return_value=['replicationcontrollers'])
@mock.patch("kubeshift.openshift.KubeBase.get_groups", side_effect=get_groups)
@mock.patch("kubeshift.openshift.KubeBase.request", side_effect=request)
@mock.patch("kubeshift.openshift.KubeBase.kind_to_resource_name", return_value='replicationcontrollers')
def test_delete_with_replicationcontroller(utest_connection, uget_resources, uget_groups, urequest, ukind_to_resource_name):
    # Mock the API class
    k8s_object = {"apiVersion": "v1", "kind": "ReplicationController", "metadata": {"labels": {"app": "helloapache"}, "name": "helloapache"}, "spec": {
        "containers": [{"image": "$image", "name": "helloapache", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}

    a = KubeOpenshiftClient(config)
    a.delete(k8s_object, "foobar")


@mock.patch("kubeshift.openshift.KubeBase.test_connection", side_effect=test_connection)
@mock.patch("kubeshift.openshift.KubeBase.get_resources", side_effect=get_resources)
@mock.patch("kubeshift.openshift.KubeBase.get_groups", side_effect=get_groups_example)
@mock.patch("kubeshift.openshift.KubeBase.request", side_effect=request)
def test_create_with_fake_kind(utest_connection, uget_resources, uget_groups, urequest):
    # Mock the API class
    k8s_object = {"apiVersion": "v1", "kind": "foobar", "metadata": {"labels": {"app": "helloapache"}, "name": "helloapache"}, "spec": {
        "containers": [{"image": "$image", "name": "helloapache", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}

    a = KubeOpenshiftClient(config)

    with pytest.raises(KubeOpenshiftError):
        a.create(k8s_object, "foobar")


@mock.patch("kubeshift.openshift.KubeBase.test_connection", side_effect=test_connection)
@mock.patch("kubeshift.openshift.KubeBase.get_resources", side_effect=get_resources)
@mock.patch("kubeshift.openshift.KubeBase.get_groups", side_effect=get_groups_example)
@mock.patch("kubeshift.openshift.KubeBase.request", side_effect=request)
def test_create_with_missing_kind(utest_connection, uget_resources, uget_groups, urequest):
    # Mock the API class
    k8s_object = {"apiVersion": "v1", "metadata": {"labels": {"app": "helloapache"}, "name": "helloapache"}, "spec": {
        "containers": [{"image": "$image", "name": "helloapache", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}

    a = KubeOpenshiftClient(config)

    with pytest.raises(KubeOpenshiftError):
        a.create(k8s_object, "foobar")


@mock.patch("kubeshift.openshift.KubeBase.test_connection", side_effect=test_connection)
@mock.patch("kubeshift.openshift.KubeBase.get_resources", side_effect=get_resources)
@mock.patch("kubeshift.openshift.KubeBase.get_groups", side_effect=get_groups_example)
@mock.patch("kubeshift.openshift.KubeBase.request", side_effect=request)
def test_create_with_missing_metadata_name(utest_connection, uget_resources, uget_groups, urequest):
    # Mock the API class
    k8s_object = {"apiVersion": "v1", "kind": "Pod", "metadata": {"labels": {"app": "helloapache"}}, "spec": {
        "containers": [{"image": "$image", "name": "helloapache", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}

    a = KubeOpenshiftClient(config)

    with pytest.raises(KubeBaseError):
        a.create(k8s_object, "foobar")


@mock.patch("kubeshift.openshift.KubeBase.test_connection", side_effect=test_connection)
@mock.patch("kubeshift.openshift.KubeBase.get_resources", side_effect=get_resources)
@mock.patch("kubeshift.openshift.KubeBase.get_groups", side_effect=get_groups)
def test_generate_kurl_with_params(utest_connection, uget_resources, uget_groups):
    k8s_object = {"apiVersion": "v1", "kind": "Pod", "metadata": {"labels": {"app": "helloapache"}, "name": "helloapache"}, "spec": {
        "containers": [{"image": "$image", "name": "helloapache", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}
    resource, url = KubeOpenshiftClient(config)._generate_kurl(
        k8s_object, 'foobar', params={'foo': 'bar'})
    assert resource == "pods"
    assert url == "http://localhost:8080/api/v1/namespaces/foobar/pods/?foo=bar"
