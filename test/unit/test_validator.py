import unittest

from kubeshift.exceptions import KubeShiftError
from kubeshift import validator


class TestValidator(unittest.TestCase):

    def test_validate_no_object(self):
        with self.assertRaises(KubeShiftError):
            validator.validate(None)

    def test_validate_not_dict(self):
        with self.assertRaises(KubeShiftError):
            validator.validate('')

    def test_validate_no_version_attr(self):
        with self.assertRaises(KubeShiftError):
            validator.validate({'kind': 'Pod'})

    def test_validate_no_kind_attr(self):
        with self.assertRaises(KubeShiftError):
            validator.validate({'apiVersion': 'v1'})

    def test_validate_no_metadata_name_attr(self):
        with self.assertRaises(KubeShiftError):
            validator.validate({'apiVersion': 'v1', 'kind': 'Pod'})

    def test_validate_success(self):
        api_version, kind, name = validator.validate(
            {'apiVersion': 'v1', 'kind': 'Pod', 'metadata': {'name': 'test'}})
        self.assertEqual(api_version, 'v1')
        self.assertEqual(kind, 'Pod')
        self.assertEqual(name, 'test')

    def test_check_url_neither_http_https(self):
        with self.assertRaises(KubeShiftError):
            validator.check_url('tcp://localhost:8080')

    def test_check_url_http(self):
        try:
            validator.check_url('http://localhost:8080')
        except KubeShiftError:
            self.fail('validator.check_url raised KubeShiftError unexpectedly')

    def test_check_url_https(self):
        try:
            validator.check_url('https://localhost:8080')
        except KubeShiftError:
            self.fail('validator.check_url raised KubeShiftError unexpectedly')
