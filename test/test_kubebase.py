import pytest
import requests
import mock
from copy import deepcopy
from kubeshift.base import KubeBase
from kubeshift.exceptions import KubeConnectionError, KubeBaseError


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
kubebase = KubeBase(config)

config_ssl = {
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
kubebase_with_ssl = KubeBase(config_ssl)


def test_config_missing_current_context():
    mod_config = deepcopy(config)
    del mod_config['current-context']
    with pytest.raises(KubeBaseError):
        KubeBase(mod_config)


def test_config_with_certificate_and_skip_tls():
    mod_config = deepcopy(config)
    mod_config['clusters'][0]['cluster']['certificate-authority'] = "/foo/bar/key.pem"
    mod_config['clusters'][0]['cluster']['insecure-skip-tls-verify'] = 'true'
    a = KubeBase(mod_config)
    assert a.certificate_authority == "/foo/bar/key.pem"
    assert a.insecure_skip_tls_verify == "true"


def test_config_with_client_key_and_certificate():
    mod_config = deepcopy(config)
    mod_config['users'][0]['user']['client-certificate'] = "/foo/bar/cert.pem"
    mod_config['users'][0]['user']['client-key'] = "/foo/bar/key.pem"
    a = KubeBase(mod_config)
    assert a.client_certification == "/foo/bar/cert.pem"
    assert a.client_key == "/foo/bar/key.pem"


def test_config_with_missing_clusters():
    mod_config = deepcopy(config)
    del mod_config['clusters']
    with pytest.raises(KubeBaseError):
        KubeBase(mod_config)


def test_config_with_missing_contexts():
    mod_config = deepcopy(config)
    del mod_config['contexts']
    with pytest.raises(KubeBaseError):
        KubeBase(mod_config)


def test_config_with_missing_users():
    mod_config = deepcopy(config)
    del mod_config['users']
    with pytest.raises(KubeBaseError):
        KubeBase(mod_config)


def test_get_resources(httpserver):
    content = '{"kind":"APIResourceList","groupVersion":"v1","resources":[{"name":"bindings","namespaced":true,"kind":"Binding"},{"name":"componentstatuses","namespaced":false,"kind":"ComponentStatus"}]}'
    httpserver.serve_content(content, code=200, headers=None)
    kubebase.get_resources(httpserver.url)


def test_get_groups(httpserver):
    content = '{"kind":"APIGroupList","groups":[{"name":"autoscaling","versions":[{"groupVersion":"autoscaling/v1","version":"v1"}],"preferredVersion":{"groupVersion":"autoscaling/v1","version":"v1"},"serverAddressByClientCIDRs":[{"clientCIDR":"0.0.0.0/0","serverAddress":"192.168.1.156:443"}]},{"name":"batch","versions":[{"groupVersion":"batch/v1","version":"v1"}],"preferredVersion":{"groupVersion":"batch/v1","version":"v1"},"serverAddressByClientCIDRs":[{"clientCIDR":"0.0.0.0/0","serverAddress":"192.168.1.156:443"}]},{"name":"extensions","versions":[{"groupVersion":"extensions/v1beta1","version":"v1beta1"}],"preferredVersion":{"groupVersion":"extensions/v1beta1","version":"v1beta1"},"serverAddressByClientCIDRs":[{"clientCIDR":"0.0.0.0/0","serverAddress":"192.168.1.156:443"}]}]}'
    httpserver.serve_content(content, code=200, headers=None)
    kubebase.get_groups(httpserver.url)


def test_connection(httpserver):
    httpserver.serve_content(content="OK", code=200, headers=None)
    kubebase.test_connection(httpserver.url)


def test_kind_to_resource_name():
    assert kubebase.kind_to_resource_name("Pod") == "pods"
    assert kubebase.kind_to_resource_name("ReplicationController") == "replicationcontrollers"
    assert kubebase.kind_to_resource_name("ImageRepository") == "imagerepositories"
    assert kubebase.kind_to_resource_name("miss") == "misses"
    assert kubebase.kind_to_resource_name("lowercase") == "lowercases"


def test_request_methods_failures():
    with pytest.raises(KubeConnectionError):
        kubebase.request("get", "http://foobar")
    with pytest.raises(KubeConnectionError):
        kubebase.request("post", "http://foobar")
    with pytest.raises(KubeConnectionError):
        kubebase.request("put", "http://foobar")
    with pytest.raises(KubeConnectionError):
        kubebase.request("delete", "http://foobar")
    with pytest.raises(KubeConnectionError):
        kubebase.request("patch", "http://foobar")


def test_request_timeout(httpserver):
    httpserver.serve_content(content="Time out", code=408, headers=None)
    with pytest.raises(KubeConnectionError):
        kubebase.request("get", httpserver.url)


def test_request_ok(httpserver):
    httpserver.serve_content(content="OK", code=200, headers=None)
    kubebase.request("get", httpserver.url)


'''
Websocket functionality does NOT work at the moment. Disabling tests until it does.

def test_websocket_request_without_ssl():
    with pytest.raises(AttributeError):
        kubebase.websocket_request("http://foobar")


def test_websocket_with_outfile(httpserver):
    httpserver.serve_content(content="OK", code=200, headers=None)
    kubebase.websocket_request(httpserver.url)
'''


def test_request_with_read_timeout():
    with pytest.raises(KubeConnectionError):
        with mock.patch('kubeshift.base.KubeBase._request_method') as fake_timeout_request:
            fake_timeout_request.side_effect = requests.exceptions.ReadTimeout(
                mock.Mock(status=404), 'not found')
            kubebase.request("get", "foobar:8080")


def test_request_with_connect_timeout():
    with pytest.raises(KubeConnectionError):
        with mock.patch('kubeshift.base.KubeBase._request_method') as fake_timeout_request:
            fake_timeout_request.side_effect = requests.exceptions.ConnectTimeout(
                mock.Mock(status=404), 'not found')
            kubebase.request("get", "foobar:8080")


def test_request_with_bad_ssl():
    with pytest.raises(KubeConnectionError):
        with mock.patch('kubeshift.base.KubeBase._request_method') as fake_timeout_request:
            fake_timeout_request.side_effect = requests.exceptions.SSLError(
                mock.Mock(status=404), 'not found')
            kubebase.request("get", "foobar:8080")


def test_cert_file_with_file_input():
    assert KubeBase.cert_file("/foo/bar", "foo") == "/foo/bar"


# Make sure that we return a /tmp file
def test_cert_file_with_plaintext_cert():
    a = KubeBase.cert_file("foo", "foo")
    assert "/tmp/" in a


# Zm9v is foo base64'd
def test_cert_file_with_base64_cert():
    a = KubeBase.cert_file("Zm9v", "foo-data")
    f = open(a, 'r')
    base64_data = f.read()
    f.close()
    assert base64_data == "foo"
