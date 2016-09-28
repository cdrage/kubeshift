import unittest

from mock import patch

from kubeshift.base import KubeBase
from kubeshift.config import Config
from kubeshift.query import Query

import helper


class TestQuery(unittest.TestCase):

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

    def test_check_methods_exist(self):
        client = KubeBase(self.config)

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

        for api in apis:
            self.assertIsNotNone(getattr(client, api, None))
            result = getattr(client, api)()
            self.assertIsInstance(result, Query)

    def test_all(self):
        client = KubeBase(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            data = client.nodes().all()
            self.assertEqual(data, {})

    def test_items(self):
        client = KubeBase(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            data = client.nodes().items()
            self.assertEqual(data, [])

    def test_metadata(self):
        client = KubeBase(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            data = client.nodes().metadata()
            self.assertEqual(data, [])

    def test_filters_no_input(self):
        client = KubeBase(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            data = client.nodes().filter()
            self.assertEqual(data, [])

    def test_filters_namespace(self):
        client = KubeBase(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            data = client.nodes().filter(namespace='default')
            self.assertEqual(data, [])

    def test_filters_status(self):
        client = KubeBase(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            data = client.nodes().filter(status='Running')
            self.assertEqual(data, [])

    def test_filters_both_inputs(self):
        client = KubeBase(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            data = client.nodes().filter(namespace='default', status='Running')
            self.assertEqual(data, [])
