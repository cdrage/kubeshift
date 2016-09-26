import copy
import json
import os

import requests
import six
import six.moves.urllib.parse as urlparse


FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')


API_MAP = {
    '/api/v1/': os.path.join(FIXTURE_DIR, 'kubernetes_resources_v1.json'),
    '/apis/': os.path.join(FIXTURE_DIR, 'kubernetes_apigroups.json'),
    '/apis/apps/v1alpha1': os.path.join(FIXTURE_DIR, 'kubernetes_resources_apps_v1alpha1.json'),
    '/apis/authentication.k8s.io/v1beta1': os.path.join(FIXTURE_DIR, 'kubernetes_resources_authentication_v1beta1.json'),
    '/apis/autoscaling/v1': os.path.join(FIXTURE_DIR, 'kubernetes_resources_autoscaling_v1.json'),
    '/apis/batch/v1': os.path.join(FIXTURE_DIR, 'kubernetes_resources_batch_v1.json'),
    '/apis/batch/v2alpha1': os.path.join(FIXTURE_DIR, 'kubernetes_resources_batch_v2alpha1.json'),
    '/apis/extensions/v1beta1': os.path.join(FIXTURE_DIR, 'kubernetes_resources_extensions_v1beta1.json'),
    '/oapi/v1/': os.path.join(FIXTURE_DIR, 'openshift_resources_v1.json'),
}


TEST_CONFIG = {
    'kind': 'Config',
    'preferences': {},
    'current-context': 'dev',
    'contexts': [
            {
                'name': 'dev',
                'context': {
                    'cluster': 'dev',
                    'user': 'default'
                }
            }
    ],
    'clusters': [
        {
            'cluster': {
                'server': 'http://localhost:8080'
            },
            'name': 'dev'
        }
    ],
    'apiVersion': 'v1',
    'users': [
        {
            'name': 'default',
            'user': {
                    'token': 'foobar'
            }
        }
    ]
}

TEST_CONFIG_NO_VERIFY = copy.deepcopy(TEST_CONFIG)
TEST_CONFIG_NO_VERIFY['clusters'][0]['cluster']['server'] = 'https://localhost:443'
TEST_CONFIG_NO_VERIFY['clusters'][0]['cluster']['insecure-skip-tls-verify'] = True

TEST_CONFIG_VERIFY = copy.deepcopy(TEST_CONFIG)
TEST_CONFIG_VERIFY['clusters'][0]['cluster']['server'] = 'https://localhost:443'
TEST_CONFIG_VERIFY['clusters'][0]['cluster']['certificate-authority'] = '/tmp/cacert.pem'


def _read_file(filepath):
    if not filepath:
        return {}

    with open(filepath, 'r') as fd:
        return json.load(fd)


def load_resource(url):
    parts = urlparse.urlparse(url)
    return _read_file(API_MAP.get(parts.path))


def get_groups(url):
    data = load_resource(url)

    groups = []
    for group in data.get('groups', []):
        for ver in group.get('versions', []):
            if ver.get('groupVersion'):
                groups.append(ver.get('groupVersion'))
    return groups


def get_resources(url):
    data = load_resource(url)
    return data.get('resources', []) if data else []


def test_connection(url):
    pass


def make_response(code, content):
    r = requests.Response()
    r.status_code = code
    if content is not None:
        r.raw = six.BytesIO(six.b(json.dumps(content)))
    return r
