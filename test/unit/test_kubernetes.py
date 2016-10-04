import os
import unittest

from mock import patch

from kubeshift.kubernetes import KubernetesClient
from kubeshift.config import Config
from kubeshift.exceptions import KubeRequestError, KubeShiftError

import helper

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')


class TestKubernetesClient(unittest.TestCase):

    def setUp(self):
        self.config = Config(helper.TEST_CONFIG)

        patched_test_connection = patch.object(KubernetesClient, '_test_connection', side_effect=helper.test_connection)
        self.addCleanup(patched_test_connection.stop)
        self.mock_tc = patched_test_connection.start()

        patched_get_groups = patch.object(KubernetesClient, '_get_groups', side_effect=helper.get_groups)
        self.addCleanup(patched_get_groups.stop)
        self.mock_groups = patched_get_groups.start()

        patched_get_resources = patch.object(KubernetesClient, '_get_resources', side_effect=helper.get_resources)
        self.addCleanup(patched_get_resources.stop)
        self.mock_resources = patched_get_resources.start()

    def test_create(self):
        client = KubernetesClient(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            try:
                client.create({'apiVersion': 'v1', 'kind': 'Pod', 'metadata': {'name': 'test'}})
            except KubeRequestError:
                self.fail('create raised KubeRequestError unexpectedly')

    def test_delete(self):
        client = KubernetesClient(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            try:
                client.delete({'apiVersion': 'v1', 'kind': 'Pod', 'metadata': {'name': 'test'}})
            except KubeRequestError:
                self.fail('delete raised KubeRequestError unexpectedly')

    def test_delete_rc(self):
        client = KubernetesClient(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            try:
                client.delete({'apiVersion': 'v1', 'kind': 'ReplicationController', 'metadata': {'name': 'test'}})
            except KubeRequestError:
                self.fail('delete raised KubeRequestError unexpectedly')

    def test_scale(self):
        client = KubernetesClient(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            try:
                client.scale({'apiVersion': 'v1', 'kind': 'Pod', 'metadata': {'name': 'test'}}, replicas=2)
            except KubeRequestError:
                self.fail('scale raised KubeRequestError unexpectedly')

    def test_replace(self):
        client = KubernetesClient(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            try:
                client.replace({'apiVersion': 'v1', 'kind': 'Pod', 'metadata': {'name': 'test'}})
            except KubeRequestError:
                self.fail('replace raised KubeRequestError unexpectedly')

    def test_modify(self):
        client = KubernetesClient(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            try:
                client.modify({'apiVersion': 'v1', 'kind': 'Pod', 'metadata': {'name': 'test'}})
            except KubeRequestError:
                self.fail('modify raised KubeRequestError unexpectedly')

    def test_create_by_file_error(self):
        client = KubernetesClient(self.config)
        with self.assertRaises(KubeShiftError):
            client.create_by_file(os.path.join(FIXTURE_DIR, 'yaml', 'fake-file.yaml'))

    def test_create_by_file_json(self):
        client = KubernetesClient(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            try:
                resp = client.create_by_file(os.path.join(FIXTURE_DIR, 'json', 'redis-master.json'))
                self.assertIsInstance(resp, list)
                self.assertEqual(len(resp), 1)
            except KubeRequestError:
                self.fail('create raised KubeRequestError unexpectedly')

    def test_create_by_file_yaml(self):
        client = KubernetesClient(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            try:
                resp = client.create_by_file(os.path.join(FIXTURE_DIR, 'yaml', 'es-rc.yaml'))
                self.assertIsInstance(resp, list)
                self.assertEqual(len(resp), 2)
            except KubeRequestError:
                self.fail('create raised KubeRequestError unexpectedly')

    def test_replace_by_file_error(self):
        client = KubernetesClient(self.config)
        with self.assertRaises(KubeShiftError):
            client.replace_by_file(os.path.join(FIXTURE_DIR, 'yaml', 'fake-file.yaml'))

    def test_replace_by_file_json(self):
        client = KubernetesClient(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            try:
                client.replace_by_file(os.path.join(FIXTURE_DIR, 'json', 'redis-slave-service.json'))
            except KubeRequestError:
                self.fail('create raised KubeRequestError unexpectedly')

    def test_replace_by_file_yaml(self):
        client = KubernetesClient(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            try:
                client.replace_by_file(os.path.join(FIXTURE_DIR, 'yaml', 'service-account.yaml'))
            except KubeRequestError:
                self.fail('create raised KubeRequestError unexpectedly')

    def test_modify_by_file_error(self):
        client = KubernetesClient(self.config)
        with self.assertRaises(KubeShiftError):
            client.modify_by_file(os.path.join(FIXTURE_DIR, 'yaml', 'fake-file.yaml'))

    def test_modify_by_file_json(self):
        client = KubernetesClient(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            try:
                client.modify_by_file(os.path.join(FIXTURE_DIR, 'json', 'redis-slave-service.json'))
            except KubeRequestError:
                self.fail('create raised KubeRequestError unexpectedly')

    def test_modify_by_file_yaml(self):
        client = KubernetesClient(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            try:
                client.modify_by_file(os.path.join(FIXTURE_DIR, 'yaml', 'service-account.yaml'))
            except KubeRequestError:
                self.fail('create raised KubeRequestError unexpectedly')

    def test_delete_by_file_error(self):
        client = KubernetesClient(self.config)
        with self.assertRaises(KubeShiftError):
            client.delete_by_file(os.path.join(FIXTURE_DIR, 'yaml', 'fake-file.yaml'))

    def test_delete_by_file_json(self):
        client = KubernetesClient(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            try:
                client.delete_by_file(os.path.join(FIXTURE_DIR, 'json', 'redis-slave-service.json'))
            except KubeRequestError:
                self.fail('create raised KubeRequestError unexpectedly')

    def test_delete_by_file_yaml(self):
        client = KubernetesClient(self.config)
        with patch.object(client.session, 'request', return_value=helper.make_response(200, {})):
            try:
                client.delete_by_file(os.path.join(FIXTURE_DIR, 'yaml', 'service-account.yaml'))
            except KubeRequestError:
                self.fail('create raised KubeRequestError unexpectedly')
