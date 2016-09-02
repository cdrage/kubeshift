import mock
import pytest
from copy import deepcopy
from kubeshift.kubernetes import KubeKubernetesClient
from kubeshift.exceptions import KubeKubernetesError

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


@mock.patch("kubeshift.kubernetes.KubeBase.test_connection", side_effect=test_connection)
@mock.patch("kubeshift.kubernetes.KubeBase.get_resources", side_effect=get_resources)
@mock.patch("kubeshift.kubernetes.KubeBase.get_groups", side_effect=get_groups)
@mock.patch("kubeshift.kubernetes.KubeBase.request", side_effect=request)
@mock.patch("kubeshift.kubernetes.KubeBase.kind_to_resource_name", return_value='Pod')
def test_create(utest_connection, uget_resources, uget_groups, urequest, ukind_to_resource_name):
    # Mock the API class
    k8s_object = {"apiVersion": "v1", "kind": "Pod", "metadata": {"labels": {"app": "helloapache"}, "name": "helloapache"}, "spec": {
        "containers": [{"image": "$image", "name": "helloapache", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}

    a = KubeKubernetesClient(config)
    a.create(k8s_object, "foobar")


@mock.patch("kubeshift.kubernetes.KubeBase.test_connection", side_effect=test_connection)
@mock.patch("kubeshift.kubernetes.KubeBase.get_resources", side_effect=get_resources)
@mock.patch("kubeshift.kubernetes.KubeBase.get_groups", side_effect=get_groups)
@mock.patch("kubeshift.kubernetes.KubeBase.request", side_effect=request)
@mock.patch("kubeshift.kubernetes.KubeBase.kind_to_resource_name", return_value='Pod')
def test_create_without_kind(utest_connection, uget_resources, uget_groups, urequest, ukind_to_resource_name):
    # Mock the API class
    k8s_object = {"apiVersion": "v1", "metadata": {"labels": {"app": "helloapache"}, "name": "helloapache"}, "spec": {
        "containers": [{"image": "$image", "name": "helloapache", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}

    a = KubeKubernetesClient(config)

    with pytest.raises(KubeKubernetesError):
        a.create(k8s_object, "foobar")


@mock.patch("kubeshift.kubernetes.KubeBase.test_connection", side_effect=test_connection)
@mock.patch("kubeshift.kubernetes.KubeBase.get_resources", side_effect=get_resources)
@mock.patch("kubeshift.kubernetes.KubeBase.get_groups", side_effect=get_groups)
@mock.patch("kubeshift.kubernetes.KubeBase.request", side_effect=request)
@mock.patch("kubeshift.kubernetes.KubeBase.kind_to_resource_name", return_value='Pod')
def test_create_without_api_version(utest_connection, uget_resources, uget_groups, urequest, ukind_to_resource_name):
    # Mock the API class
    k8s_object = {"kind": "Pod", "metadata": {"labels": {"app": "helloapache"}, "name": "helloapache"}, "spec": {
        "containers": [{"image": "$image", "name": "helloapache", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}

    a = KubeKubernetesClient(config)

    with pytest.raises(KubeKubernetesError):
        a.create(k8s_object, "foobar")


@mock.patch("kubeshift.kubernetes.KubeBase.test_connection", side_effect=test_connection)
@mock.patch("kubeshift.kubernetes.KubeBase.get_resources", side_effect=get_resources)
@mock.patch("kubeshift.kubernetes.KubeBase.get_groups", side_effect=get_groups_example)
@mock.patch("kubeshift.kubernetes.KubeBase.request", side_effect=request)
@mock.patch("kubeshift.kubernetes.KubeBase.kind_to_resource_name", return_value='Pod')
def test_create_with_v1beta1(utest_connection, uget_resources, uget_groups, urequest, ukind_to_resource_name):
    # Mock the API class
    k8s_object = {"apiVersion": "extensions/v1beta1", "kind": "Pod", "metadata": {"labels": {"app": "helloapache"}, "name": "helloapache"}, "spec": {
        "containers": [{"image": "$image", "name": "helloapache", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}

    a = KubeKubernetesClient(config)

    a.create(k8s_object, "foobar")


@mock.patch("kubeshift.kubernetes.KubeBase.test_connection", side_effect=test_connection)
@mock.patch("kubeshift.kubernetes.KubeBase.get_resources", side_effect=get_resources)
@mock.patch("kubeshift.kubernetes.KubeBase.get_groups", side_effect=get_groups_example)
@mock.patch("kubeshift.kubernetes.KubeBase.request", side_effect=request)
def test_create_with_fake_kind(utest_connection, uget_resources, uget_groups, urequest):
    # Mock the API class
    k8s_object = {"apiVersion": "v1", "kind": "foobar", "metadata": {"labels": {"app": "helloapache"}, "name": "helloapache"}, "spec": {
        "containers": [{"image": "$image", "name": "helloapache", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}

    a = KubeKubernetesClient(config)

    with pytest.raises(KubeKubernetesError):
        a.create(k8s_object, "foobar")


@mock.patch("kubeshift.kubernetes.KubeBase.test_connection", side_effect=test_connection)
@mock.patch("kubeshift.kubernetes.KubeBase.get_resources", side_effect=get_resources)
@mock.patch("kubeshift.kubernetes.KubeBase.get_groups", side_effect=get_groups_example)
@mock.patch("kubeshift.kubernetes.KubeBase.request", side_effect=request)
def test_create_with_missing_metadata_name(utest_connection, uget_resources, uget_groups, urequest):
    # Mock the API class
    k8s_object = {"apiVersion": "v1", "kind": "Pod", "metadata": {"labels": {"app": "helloapache"}}, "spec": {
        "containers": [{"image": "$image", "name": "helloapache", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}

    a = KubeKubernetesClient(config)

    with pytest.raises(KubeKubernetesError):
        a.create(k8s_object, "foobar")


@mock.patch("kubeshift.kubernetes.KubeBase.test_connection", side_effect=test_connection)
@mock.patch("kubeshift.kubernetes.KubeBase.get_resources", side_effect=get_resources)
@mock.patch("kubeshift.kubernetes.KubeBase.get_groups", side_effect=get_groups)
@mock.patch("kubeshift.kubernetes.KubeBase.request", side_effect=request)
@mock.patch("kubeshift.kubernetes.KubeBase.kind_to_resource_name", return_value='Pod')
def test_delete(utest_connection, uget_resources, uget_groups, urequest, ukind_to_resource_name):
    # Mock the API class
    k8s_object = {"apiVersion": "v1", "kind": "Pod", "metadata": {"labels": {"app": "helloapache"}, "name": "helloapache"}, "spec": {
        "containers": [{"image": "$image", "name": "helloapache", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}

    a = KubeKubernetesClient(config)
    a.delete(k8s_object, "foobar")


@mock.patch("kubeshift.kubernetes.KubeBase.test_connection", side_effect=test_connection)
@mock.patch("kubeshift.kubernetes.KubeBase.get_resources", return_value=['replicationcontrollers'])
@mock.patch("kubeshift.kubernetes.KubeBase.get_groups", side_effect=get_groups)
@mock.patch("kubeshift.kubernetes.KubeBase.request", side_effect=request)
@mock.patch("kubeshift.kubernetes.KubeBase.kind_to_resource_name", return_value='replicationcontrollers')
def test_delete_with_replicationcontroller(utest_connection, uget_resources, uget_groups, urequest, ukind_to_resource_name):
    # Mock the API class
    k8s_object = {"apiVersion": "v1", "kind": "ReplicationController", "metadata": {"labels": {"app": "helloapache"}, "name": "helloapache"}, "spec": {
        "containers": [{"image": "$image", "name": "helloapache", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}

    a = KubeKubernetesClient(config)
    a.delete(k8s_object, "foobar")


@mock.patch("kubeshift.kubernetes.KubeBase.test_connection", side_effect=test_connection)
@mock.patch("kubeshift.kubernetes.KubeBase.get_resources", return_value=['replicationcontrollers'])
@mock.patch("kubeshift.kubernetes.KubeBase.get_groups", side_effect=get_groups)
@mock.patch("kubeshift.kubernetes.KubeBase.request", side_effect=request)
@mock.patch("kubeshift.kubernetes.KubeBase.kind_to_resource_name", return_value='replicationcontrollers')
def test_scale(utest_connection, uget_resources, uget_groups, urequest, ukind_to_resource_name):
    # Mock the API class
    k8s_object = {"apiVersion": "v1", "kind": "ReplicationController", "metadata": {"labels": {"app": "helloapache"}, "name": "helloapache"}, "spec": {
        "containers": [{"image": "$image", "name": "helloapache", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}

    a = KubeKubernetesClient(config)
    a.scale(k8s_object, "foobar")


def test_init_non_http():
    mod_config = deepcopy(config)
    mod_config['clusters'][0]['cluster']['server'] = "foo"
    with pytest.raises(KubeKubernetesError):
        KubeKubernetesClient(mod_config)


@mock.patch("kubeshift.kubernetes.KubeBase.test_connection", side_effect=test_connection)
@mock.patch("kubeshift.kubernetes.KubeBase.get_resources", side_effect=get_resources)
@mock.patch("kubeshift.kubernetes.KubeBase.get_groups", side_effect=get_groups_example)
def test_init_with_groups(utest_connection, uget_resources, uget_groups):
    KubeKubernetesClient(config)


@mock.patch("kubeshift.kubernetes.KubeBase.test_connection", side_effect=test_connection)
@mock.patch("kubeshift.kubernetes.KubeBase.get_resources", side_effect=get_resources)
@mock.patch("kubeshift.kubernetes.KubeBase.get_groups", side_effect=get_groups)
def test_generate_kurl_with_params(utest_connection, uget_resources, uget_groups):
    k8s_object = {"apiVersion": "v1", "kind": "Pod", "metadata": {"labels": {"app": "helloapache"}, "name": "helloapache"}, "spec": {
        "containers": [{"image": "$image", "name": "helloapache", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}
    resource, url = KubeKubernetesClient(config)._generate_kurl(k8s_object, 'foobar', params={'foo': 'bar'})
    assert resource == "pods"
    assert url == "http://localhost:8080/api/v1/namespaces/foobar/pods/?foo=bar"
