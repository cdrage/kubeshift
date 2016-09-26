import unittest

from mock import patch
import requests

from kubeshift.base import KubeBase
from kubeshift.config import Config
from kubeshift.exceptions import (KubeConnectionError, KubeRequestError, KubeShiftError)

import helper


class FakeKubeBase(KubeBase):

    def __init__(self, *args, **kwargs):

        self.kubeconfig = Config(helper.TEST_CONFIG)
        self.base_url = self.kubeconfig.cluster.get('server')

        self.session = self._connection()
        self.api_resources = {}

    def request(self, method, url, data=None):
        return helper.load_resource(url)


class TestBaseResources(unittest.TestCase):

    def setUp(self):
        self.client = FakeKubeBase(Config(helper.TEST_CONFIG))

    def test_test_connection(self):
        self.client._test_connection(self.client.base_url)

    def test_get_resources(self):
        resource = self.client._get_resources(self.client.base_url + '/apis/batch/v1')
        self.assertTrue(resource)
        self.assertIsInstance(resource, list)
        self.assertEqual(len(resource), 2)
        self.assertEqual(resource, [
            {
                'name': 'jobs',
                'namespaced': True,
                'kind': 'Job'
            },
            {
                'name': 'jobs/status',
                'namespaced': True,
                'kind': 'Job'
            }]
        )

    def test_get_groups(self):
        groups = self.client._get_groups(self.client.base_url + '/apis/')
        self.assertTrue(groups)
        self.assertIsInstance(groups, list)
        self.assertEqual(len(groups), 6)

    def test_get_groups_empty(self):
        groups = self.client._get_groups(self.client.base_url + '/others/')
        self.assertFalse(groups)
        self.assertIsInstance(groups, list)
        self.assertEqual(len(groups), 0)

    def test_generate_url_fail(self):
        self.client._load_group_resources('apis/')
        self.assertRaises(KubeShiftError, self.client._generate_url, self.client, 'extensions/v1beta1', 'Fake')

    def test_generate_url_namespace(self):
        self.client._load_group_resources('apis/')
        url = self.client._generate_url('batch/v1', 'Job', 'default')
        self.assertEqual(url, 'http://localhost:8080/apis/batch/v1/namespaces/default/jobs')

    def test_generate_url_wo_namespace(self):
        self.client._load_resources('api/v1/', 'v1')
        url = self.client._generate_url('v1', 'Node', None)
        self.assertEqual(url, 'http://localhost:8080/api/v1/nodes')

    def test_generate_url_name(self):
        self.client._load_group_resources('apis/')
        url = self.client._generate_url('batch/v1', 'Job', 'default', 'testjob')
        self.assertEqual(url, 'http://localhost:8080/apis/batch/v1/namespaces/default/jobs/testjob')

    def test_generate_url_params_dict(self):
        self.client._load_resources('api/v1/', 'v1')
        url = self.client._generate_url('v1', 'Pod', 'sample', None, {'labelSelector': 'name=test'})
        self.assertEqual(url, 'http://localhost:8080/api/v1/namespaces/sample/pods?labelSelector=name%3Dtest')

    def test_generate_url_params_sequence(self):
        self.client._load_resources('api/v1/', 'v1')
        url = self.client._generate_url('v1', 'Pod', 'sample', None, [('labelSelector', 'name=test')])
        self.assertEqual(url, 'http://localhost:8080/api/v1/namespaces/sample/pods?labelSelector=name%3Dtest')


class TestClientBase(unittest.TestCase):

    def setUp(self):
        self.config = Config(helper.TEST_CONFIG)

        patched_test_connection = patch.object(KubeBase, '_test_connection', side_effect=helper.test_connection)
        self.addCleanup(patched_test_connection.stop)
        self.mock_tc = patched_test_connection.start()

        patched_get_groups = patch.object(KubeBase, '_get_groups', side_effect=helper.get_groups)
        self.addCleanup(patched_get_groups.stop)
        self.mock_groups = patched_get_groups.start()

        patched_get_resources = patch.object(KubeBase, '_get_resources', side_effect=helper.get_resources)
        self.addCleanup(patched_get_resources.stop)
        self.mock_resources = patched_get_resources.start()

    def test_constructor_with_config_object(self):
        client = KubeBase(self.config)
        self.assertTrue(client.api_resources)

    def test_constructor_with_no_config(self):
        client = KubeBase(None)
        self.assertTrue(client.api_resources)

    def test_constructor_cert_verify(self):
        client = KubeBase(helper.TEST_CONFIG_VERIFY)
        self.assertTrue(client.api_resources)

    def test_constructor_cert_no_verify(self):
        client = KubeBase(helper.TEST_CONFIG_NO_VERIFY)
        self.assertTrue(client.api_resources)

    def test_request_ssl_error(self):
        client = KubeBase(self.config)
        with patch.object(client.session, 'request', side_effect=requests.exceptions.SSLError):
            with self.assertRaises(KubeConnectionError):
                client.request('get', 'http://localhost:8080')

    def test_request_connect_timeout(self):
        client = KubeBase(self.config)
        with patch.object(client.session, 'request', side_effect=requests.exceptions.ConnectTimeout):
            with self.assertRaises(KubeConnectionError):
                client.request('get', 'http://localhost:8080')

    def test_request_read_timeout(self):
        client = KubeBase(self.config)
        with patch.object(client.session, 'request', side_effect=requests.exceptions.ReadTimeout):
            with self.assertRaises(KubeConnectionError):
                client.request('get', 'http://localhost:8080')

    def test_request_connection_error(self):
        client = KubeBase(self.config)
        with patch.object(client.session, 'request', side_effect=requests.exceptions.ConnectionError):
            with self.assertRaises(KubeConnectionError):
                client.request('get', 'http://localhost:8080')

    def test_request_response_error(self):
        client = KubeBase(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(400, None)):
            with self.assertRaises(KubeRequestError):
                client.request('get', 'http://localhost:8080')

    def test_request_no_data(self):
        client = KubeBase(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, None)):
            data = client.request('get', 'http://localhost:8080')
            self.assertIsNone(data)

    def test_request_patch(self):
        client = KubeBase(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(201, {})):
            data = client.request('patch', 'http://localhost:8080', [
                {'op': 'replace', 'path': '/spec/replicas', 'value': 0}
            ])
            self.assertEqual(data, {})


if __name__ == '__main__':
    unittest.main()
