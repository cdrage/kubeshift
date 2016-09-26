import unittest

from mock import patch

from kubeshift.openshift import OpenshiftClient
from kubeshift.config import Config
from kubeshift.exceptions import KubeRequestError

import helper


class TestOpenshiftClient(unittest.TestCase):

    def setUp(self):
        self.config = Config(helper.TEST_CONFIG)

        patched_test_connection = patch.object(OpenshiftClient, '_test_connection', side_effect=helper.test_connection)
        self.addCleanup(patched_test_connection.stop)
        self.mock_tc = patched_test_connection.start()

        patched_get_groups = patch.object(OpenshiftClient, '_get_groups', side_effect=helper.get_groups)
        self.addCleanup(patched_get_groups.stop)
        self.mock_groups = patched_get_groups.start()

        patched_get_resources = patch.object(OpenshiftClient, '_get_resources', side_effect=helper.get_resources)
        self.addCleanup(patched_get_resources.stop)
        self.mock_resources = patched_get_resources.start()

    def test_create(self):
        client = OpenshiftClient(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            try:
                client.create({'apiVersion': 'v1', 'kind': 'BuildConfig', 'metadata': {'name': 'test'}})
            except KubeRequestError:
                self.fail('create raised KubeRequestError unexpectedly')

    def test_create_template(self):
        client = OpenshiftClient(self.config)
        template = {'apiVersion': 'v1', 'kind': 'Template', 'metadata': {'name': 'test'}, 'objects': [
            {'apiVersion': 'v1', 'kind': 'BuildConfig', 'metadata': {'name': 'test'}}
        ]}
        with patch.object(client.session, 'request', return_value=helper.make_response(200, template)):
            try:
                client.create(template)
            except KubeRequestError:
                self.fail('create raised KubeRequestError unexpectedly')

    def test_delete(self):
        client = OpenshiftClient(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            try:
                client.delete({'apiVersion': 'v1', 'kind': 'BuildConfig', 'metadata': {'name': 'test'}})
            except KubeRequestError:
                self.fail('delete raised KubeRequestError unexpectedly')

    def test_delete_template(self):
        client = OpenshiftClient(self.config)
        template = {'apiVersion': 'v1', 'kind': 'Template', 'metadata': {'name': 'test'}, 'objects': [
            {'apiVersion': 'v1', 'kind': 'BuildConfig', 'metadata': {'name': 'test'}}
        ]}
        with patch.object(client.session, 'request', return_value=helper.make_response(200, template)):
            try:
                client.delete(template)
            except KubeRequestError:
                self.fail('delete raised KubeRequestError unexpectedly')

    def test_delete_rc(self):
        client = OpenshiftClient(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            try:
                client.delete({'apiVersion': 'v1', 'kind': 'ReplicationController', 'metadata': {'name': 'test'}})
            except KubeRequestError:
                self.fail('delete raised KubeRequestError unexpectedly')

    def test_scale(self):
        client = OpenshiftClient(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            try:
                client.scale({'apiVersion': 'v1', 'kind': 'DeploymentConfig', 'metadata': {'name': 'test'}}, replicas=2)
            except KubeRequestError:
                self.fail('scale raised KubeRequestError unexpectedly')
