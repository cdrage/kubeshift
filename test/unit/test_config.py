import copy
import os
import shutil
import tempfile
import unittest

from kubeshift.config import Config

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')
CONFIG_FILE = os.path.join(tempfile.gettempdir(), '.kube', 'config')


def remove_file(name):
    try:
        os.remove(name)
    except Exception:
        pass


class TestConfig(unittest.TestCase):

    def setUp(self):
        try:
            # copy certs to /tmp directory
            shutil.copytree(
                os.path.join(FIXTURE_DIR, 'certs'),
                os.path.join(tempfile.gettempdir(), '.minikube')
            )
        except Exception:
            pass

    def tearDown(self):
        # remove certs from /tmp directory
        shutil.rmtree(os.path.join(tempfile.gettempdir(), '.minikube'), True)
        shutil.rmtree(os.path.dirname(CONFIG_FILE), True)

    def test_from_file_none(self):

        cfg = Config.from_file(None)

        self.assertIsNotNone(cfg)
        self.assertIsNone(cfg.current_context)

        self.assertIsInstance(cfg.contexts, dict)
        self.assertEqual(len(cfg.contexts), 0)
        self.assertIsInstance(cfg.clusters, dict)
        self.assertEqual(len(cfg.clusters), 0)
        self.assertIsInstance(cfg.users, dict)
        self.assertEqual(len(cfg.users), 0)

        self.assertIsInstance(cfg.context, dict)
        self.assertEqual(len(cfg.context), 0)
        self.assertIsInstance(cfg.cluster, dict)
        self.assertEqual(len(cfg.cluster), 0)
        self.assertIsInstance(cfg.user, dict)
        self.assertEqual(len(cfg.user), 0)

    def test_from_file_empty_string(self):

        cfg = Config.from_file('')

        self.assertIsNotNone(cfg)
        self.assertIsNone(cfg.current_context)

        self.assertIsInstance(cfg.contexts, dict)
        self.assertEqual(len(cfg.contexts), 0)
        self.assertIsInstance(cfg.clusters, dict)
        self.assertEqual(len(cfg.clusters), 0)
        self.assertIsInstance(cfg.users, dict)
        self.assertEqual(len(cfg.users), 0)

        self.assertIsInstance(cfg.context, dict)
        self.assertEqual(len(cfg.context), 0)
        self.assertIsInstance(cfg.cluster, dict)
        self.assertEqual(len(cfg.cluster), 0)
        self.assertIsInstance(cfg.user, dict)
        self.assertEqual(len(cfg.user), 0)

    def test_from_file_empty_file(self):

        cfg = Config.from_file(os.path.join(FIXTURE_DIR, 'empty_kubeconfig'))

        self.assertIsNotNone(cfg)
        self.assertIsNone(cfg.current_context)

        self.assertIsInstance(cfg.contexts, dict)
        self.assertEqual(len(cfg.contexts), 0)
        self.assertIsInstance(cfg.clusters, dict)
        self.assertEqual(len(cfg.clusters), 0)
        self.assertIsInstance(cfg.users, dict)
        self.assertEqual(len(cfg.users), 0)

        self.assertIsInstance(cfg.context, dict)
        self.assertEqual(len(cfg.context), 0)
        self.assertIsInstance(cfg.cluster, dict)
        self.assertEqual(len(cfg.cluster), 0)
        self.assertIsInstance(cfg.user, dict)
        self.assertEqual(len(cfg.user), 0)

    def test_from_file_simple(self):

        cfg = Config.from_file(os.path.join(FIXTURE_DIR, 'simple_kubeconfig'))

        self.assertIsNotNone(cfg)
        self.assertEqual(cfg.current_context, 'default/192-168-99-103:8443/admin')

        self.assertIsInstance(cfg.contexts, dict)
        self.assertEqual(len(cfg.contexts), 1)
        self.assertIsInstance(cfg.clusters, dict)
        self.assertEqual(len(cfg.clusters), 1)
        self.assertIsInstance(cfg.users, dict)
        self.assertEqual(len(cfg.users), 1)

        self.assertIsInstance(cfg.context, dict)
        self.assertEqual(
            cfg.context,
            {
                'cluster': '192-168-99-103:8443',
                'namespace': 'default',
                'user': 'admin/192-168-99-103:8443'
            }
        )
        self.assertIsInstance(cfg.cluster, dict)
        self.assertEqual(
            cfg.cluster,
            {
                'insecure-skip-tls-verify': True,
                'server': 'https://192.168.99.103:8443'
            }
        )
        self.assertIsInstance(cfg.user, dict)
        self.assertEqual(
            cfg.user,
            {
                'token': 'qgfe3Z3nJPAtTS_OsNeThQEwzRvwSkHenxd4lS_x0RM'
            }
        )

    def test_format_session_no_context(self):

        cfg = Config.from_file(os.path.join(FIXTURE_DIR, 'empty_kubeconfig'))

        self.assertIsNotNone(cfg)
        self.assertIsNone(cfg.current_context)
        self.assertEqual(
            cfg.format_session(),
            {
                'cert': None,
                'headers': {},
                'verify': True
            }
        )

    def test_format_session_token(self):

        cfg = Config.from_file(os.path.join(FIXTURE_DIR, 'simple_kubeconfig'))

        self.assertIsNotNone(cfg)
        self.assertEqual(cfg.current_context, 'default/192-168-99-103:8443/admin')
        self.assertEqual(
            cfg.format_session(),
            {
                'cert': None,
                'headers': {
                    'Authorization': 'Bearer qgfe3Z3nJPAtTS_OsNeThQEwzRvwSkHenxd4lS_x0RM'
                },
                'verify': False
            }
        )

    def test_format_session_certs(self):

        cfg = Config.from_file(os.path.join(FIXTURE_DIR, 'certs_kubeconfig'))

        self.assertIsNotNone(cfg)
        self.assertEqual(cfg.current_context, 'minikube')
        self.assertEqual(
            cfg.format_session(),
            {
                'cert': (
                    '/tmp/.minikube/apiserver.crt',
                    '/tmp/.minikube/apiserver.key'
                ),
                'headers': {},
                'verify': '/tmp/.minikube/ca.crt'
            }
        )

    def test_format_session_certs_no_user(self):

        cfg = Config.from_file(os.path.join(FIXTURE_DIR, 'certs_no_user_kubeconfig'))

        self.assertIsNotNone(cfg)
        self.assertEqual(cfg.current_context, 'minishift')

        session = cfg.format_session()
        self.assertIsNone(session['cert'])
        self.assertEqual(session['headers'], {})
        # indicates it was a base64 encoded cert that was written
        # to a tempfile
        self.assertTrue(session['verify'].startswith('/tmp/'))

        # clean up the test file
        self.addCleanup(remove_file, session['verify'])

    def test_format_session_certs_data(self):

        cfg = Config.from_file(os.path.join(FIXTURE_DIR, 'certs_data_kubeconfig'))

        self.assertIsNotNone(cfg)
        self.assertEqual(cfg.current_context, 'default/192-168-99-103:8443/admin')

        session = cfg.format_session()
        self.assertIsNone(session['cert'])
        self.assertEqual(session['headers'], {
            'Authorization': 'Bearer 10me0gx3el9uHDfF7JdksZO_rEuBt_JuAZLrT0htoe4'
        })
        # indicates it was a base64 encoded cert that was written
        # to a tempfile
        self.assertTrue(session['verify'].startswith('/tmp/'))

        # clean up the test file
        self.addCleanup(remove_file, session['verify'])

    def test_from_params_none(self):

        cfg = Config.from_params()

        self.assertIsNotNone(cfg)
        self.assertEqual(cfg.current_context, 'self')

        self.assertIsInstance(cfg.contexts, dict)
        self.assertEqual(len(cfg.contexts), 1)
        self.assertIsInstance(cfg.clusters, dict)
        self.assertEqual(len(cfg.clusters), 1)
        self.assertIsInstance(cfg.users, dict)
        self.assertEqual(len(cfg.users), 1)

        self.assertIsInstance(cfg.context, dict)
        self.assertEqual(cfg.context, {
            'cluster': 'self',
            'user': 'self'
        })
        self.assertIsInstance(cfg.cluster, dict)
        self.assertEqual(cfg.cluster, {})
        self.assertIsInstance(cfg.user, dict)
        self.assertEqual(cfg.user, {})

    def test_from_params_api_only(self):

        cfg = Config.from_params(api='http://localhost')

        self.assertIsNotNone(cfg)
        self.assertEqual(cfg.current_context, 'self')

        self.assertIsInstance(cfg.contexts, dict)
        self.assertEqual(len(cfg.contexts), 1)
        self.assertIsInstance(cfg.clusters, dict)
        self.assertEqual(len(cfg.clusters), 1)
        self.assertIsInstance(cfg.users, dict)
        self.assertEqual(len(cfg.users), 1)

        self.assertIsInstance(cfg.context, dict)
        self.assertEqual(cfg.context, {
            'cluster': 'self',
            'user': 'self'
        })
        self.assertIsInstance(cfg.cluster, dict)
        self.assertEqual(cfg.cluster, {
            'server': 'http://localhost'
        })
        self.assertIsInstance(cfg.user, dict)
        self.assertEqual(cfg.user, {})

    def test_from_params_api_verify(self):

        cfg = Config.from_params(api='http://localhost', verify=False)

        self.assertIsNotNone(cfg)
        self.assertEqual(cfg.current_context, 'self')

        self.assertIsInstance(cfg.contexts, dict)
        self.assertEqual(len(cfg.contexts), 1)
        self.assertIsInstance(cfg.clusters, dict)
        self.assertEqual(len(cfg.clusters), 1)
        self.assertIsInstance(cfg.users, dict)
        self.assertEqual(len(cfg.users), 1)

        self.assertIsInstance(cfg.context, dict)
        self.assertEqual(cfg.context, {
            'cluster': 'self',
            'user': 'self'
        })
        self.assertIsInstance(cfg.cluster, dict)
        self.assertEqual(cfg.cluster, {
            'server': 'http://localhost',
            'insecure-skip-tls-verify': True
        })
        self.assertIsInstance(cfg.user, dict)
        self.assertEqual(cfg.user, {})

    def test_from_params_api_ca(self):

        cfg = Config.from_params(api='http://localhost', ca='/tmp/.minikube/ca.crt')

        self.assertIsNotNone(cfg)
        self.assertEqual(cfg.current_context, 'self')

        self.assertIsInstance(cfg.contexts, dict)
        self.assertEqual(len(cfg.contexts), 1)
        self.assertIsInstance(cfg.clusters, dict)
        self.assertEqual(len(cfg.clusters), 1)
        self.assertIsInstance(cfg.users, dict)
        self.assertEqual(len(cfg.users), 1)

        self.assertIsInstance(cfg.context, dict)
        self.assertEqual(cfg.context, {
            'cluster': 'self',
            'user': 'self'
        })
        self.assertIsInstance(cfg.cluster, dict)
        self.assertEqual(cfg.cluster, {
            'server': 'http://localhost',
            'certificate-authority': '/tmp/.minikube/ca.crt'
        })
        self.assertIsInstance(cfg.user, dict)
        self.assertEqual(cfg.user, {})

    def test_from_params_auth_token(self):

        cfg = Config.from_params(auth='qgfe3Z3nJPAtTS_OsNeThQEwzRvwSkHenxd4lS_x0RM')

        self.assertIsNotNone(cfg)
        self.assertEqual(cfg.current_context, 'self')

        self.assertIsInstance(cfg.contexts, dict)
        self.assertEqual(len(cfg.contexts), 1)
        self.assertIsInstance(cfg.clusters, dict)
        self.assertEqual(len(cfg.clusters), 1)
        self.assertIsInstance(cfg.users, dict)
        self.assertEqual(len(cfg.users), 1)

        self.assertIsInstance(cfg.context, dict)
        self.assertEqual(cfg.context, {
            'cluster': 'self',
            'user': 'self'
        })
        self.assertIsInstance(cfg.cluster, dict)
        self.assertEqual(cfg.cluster, {})
        self.assertIsInstance(cfg.user, dict)
        self.assertEqual(cfg.user, {
            'token': 'qgfe3Z3nJPAtTS_OsNeThQEwzRvwSkHenxd4lS_x0RM'
        })

    def test_from_params_auth_certs(self):

        cfg = Config.from_params(auth={
            'client-certificate': '/tmp/.minikube/apiserver.crt',
            'client-key': '/tmp/.minikube/apiserver.key'})

        self.assertIsNotNone(cfg)
        self.assertEqual(cfg.current_context, 'self')

        self.assertIsInstance(cfg.contexts, dict)
        self.assertEqual(len(cfg.contexts), 1)
        self.assertIsInstance(cfg.clusters, dict)
        self.assertEqual(len(cfg.clusters), 1)
        self.assertIsInstance(cfg.users, dict)
        self.assertEqual(len(cfg.users), 1)

        self.assertIsInstance(cfg.context, dict)
        self.assertEqual(cfg.context, {
            'cluster': 'self',
            'user': 'self'
        })
        self.assertIsInstance(cfg.cluster, dict)
        self.assertEqual(cfg.cluster, {})
        self.assertIsInstance(cfg.user, dict)
        self.assertEqual(cfg.user, {
            'client-certificate': '/tmp/.minikube/apiserver.crt',
            'client-key': '/tmp/.minikube/apiserver.key'
        })

    def test_from_params_auth_clientcert(self):

        cfg = Config.from_params(
            auth={'client-certificate': '/tmp/.minikube/apiserver.crt'},
            username='admin'
        )

        self.assertIsNotNone(cfg)
        self.assertEqual(cfg.current_context, 'self')

        self.assertIsInstance(cfg.contexts, dict)
        self.assertEqual(len(cfg.contexts), 1)
        self.assertIsInstance(cfg.clusters, dict)
        self.assertEqual(len(cfg.clusters), 1)
        self.assertIsInstance(cfg.users, dict)
        self.assertEqual(len(cfg.users), 1)

        self.assertIsInstance(cfg.context, dict)
        self.assertEqual(cfg.context, {
            'cluster': 'self',
            'user': 'admin'
        })
        self.assertIsInstance(cfg.cluster, dict)
        self.assertEqual(cfg.cluster, {})
        self.assertIsInstance(cfg.user, dict)
        self.assertEqual(cfg.user, {
            'client-certificate': '/tmp/.minikube/apiserver.crt'
        })

    def test_from_params_auth_clientkey(self):

        cfg = Config.from_params(auth={'client-key': '/tmp/.minikube/apiserver.key'})

        self.assertIsNotNone(cfg)
        self.assertEqual(cfg.current_context, 'self')

        self.assertIsInstance(cfg.contexts, dict)
        self.assertEqual(len(cfg.contexts), 1)
        self.assertIsInstance(cfg.clusters, dict)
        self.assertEqual(len(cfg.clusters), 1)
        self.assertIsInstance(cfg.users, dict)
        self.assertEqual(len(cfg.users), 1)

        self.assertIsInstance(cfg.context, dict)
        self.assertEqual(cfg.context, {
            'cluster': 'self',
            'user': 'self'
        })
        self.assertIsInstance(cfg.cluster, dict)
        self.assertEqual(cfg.cluster, {})
        self.assertIsInstance(cfg.user, dict)
        self.assertEqual(cfg.user, {
            'client-key': '/tmp/.minikube/apiserver.key'
        })

    def test_from_params_all(self):

        cfg = Config.from_params(
            api='http://localhost',
            ca='/tmp/.minikube/ca.crt',
            auth={
                'client-certificate': '/tmp/.minikube/apiserver.crt',
                'client-key': '/tmp/.minikube/apiserver.key'},
            filepath=CONFIG_FILE)

        self.assertIsNotNone(cfg)
        self.assertEqual(cfg.current_context, 'self')

        self.assertIsInstance(cfg.contexts, dict)
        self.assertEqual(len(cfg.contexts), 1)
        self.assertIsInstance(cfg.clusters, dict)
        self.assertEqual(len(cfg.clusters), 1)
        self.assertIsInstance(cfg.users, dict)
        self.assertEqual(len(cfg.users), 1)

        self.assertIsInstance(cfg.context, dict)
        self.assertEqual(cfg.context, {
            'cluster': 'self',
            'user': 'self'
        })
        self.assertIsInstance(cfg.cluster, dict)
        self.assertEqual(cfg.cluster, {
            'server': 'http://localhost',
            'certificate-authority': '/tmp/.minikube/ca.crt'
        })
        self.assertIsInstance(cfg.user, dict)
        self.assertEqual(cfg.user, {
            'client-certificate': '/tmp/.minikube/apiserver.crt',
            'client-key': '/tmp/.minikube/apiserver.key'
        })

    def test_from_param_ctx_not_found(self):
        cfg = Config.from_params(context_name='test')

        self.assertIsNotNone(cfg)
        self.assertEqual(cfg.current_context, 'test')

        self.assertIsInstance(cfg.contexts, dict)
        self.assertEqual(len(cfg.contexts), 1)
        self.assertIsInstance(cfg.clusters, dict)
        self.assertEqual(len(cfg.clusters), 1)
        self.assertIsInstance(cfg.users, dict)
        self.assertEqual(len(cfg.users), 1)

        self.assertIsInstance(cfg.context, dict)
        self.assertEqual(cfg.context, {
            'cluster': 'self',
            'user': 'self'
        })
        self.assertIsInstance(cfg.cluster, dict)
        self.assertEqual(cfg.cluster, {})
        self.assertIsInstance(cfg.user, dict)
        self.assertEqual(cfg.user, {})

    def test_from_param_ctx_found(self):
        test_file = '/tmp/.test_kc/config'
        self.addCleanup(remove_file, test_file)

        cfg = Config.from_params(filepath=test_file)

        self.assertIsNotNone(cfg)
        self.assertEqual(cfg.current_context, 'self')

        cfg.set_cluster('other')
        cfg.set_credentials('other')
        cfg.set_context('other', cluster='other', user='other')
        cfg.set_current_context('other')
        self.assertEqual('other', cfg.current_context)

        cfg.write_file()

        cfg = Config.from_params(context_name='other', filepath=test_file)

        self.assertIsInstance(cfg.context, dict)
        self.assertEqual(cfg.context, {
            'cluster': 'other',
            'user': 'other'
        })
        self.assertIsInstance(cfg.cluster, dict)
        self.assertEqual(cfg.cluster, {})
        self.assertIsInstance(cfg.user, dict)
        self.assertEqual(cfg.user, {})

        cfg.write_file()

    def test_write_file(self):

        cfg = Config.from_params(
            api='http://localhost',
            ca='/tmp/.minikube/ca.crt',
            auth={
                'client-certificate': '/tmp/.minikube/apiserver.crt',
                'client-key': '/tmp/.minikube/apiserver.key'},
            filepath=CONFIG_FILE)

        self.assertIsNotNone(cfg)

        self.assertFalse(os.path.exists(CONFIG_FILE))
        cfg.write_file()
        self.assertTrue(os.path.exists(CONFIG_FILE))
        cfg.write_file()
        self.assertTrue(os.path.exists(CONFIG_FILE))

    def test_add_item(self):
        cfg = Config.from_params()

        orig = copy.deepcopy(cfg.content)
        cfg.set_cluster(None)
        cfg.set_credentials(None)
        cfg.set_context(None, cluster='self', user='self')
        cfg.set_current_context('self')
        self.assertEqual(orig, cfg.content)

        cfg.set_current_context('other')
        self.assertNotEqual('other', cfg.current_context)

        cfg.set_cluster('other')
        cfg.set_credentials('other')
        cfg.set_context('other', cluster='other', user='other')
        cfg.set_current_context('other')
        self.assertEqual('other', cfg.current_context)

        cfg = Config({'apiVersion': 'v1'})
        self.assertIsNotNone(cfg)
        self.assertIsNone(cfg.current_context)
        self.assertNotIn('contexts', cfg.content)
        self.assertNotIn('clusters', cfg.content)
        self.assertNotIn('users', cfg.content)

        cfg.set_cluster(None)
        cfg.set_credentials(None)
        cfg.set_context(None, cluster='self', user='self')
        cfg.set_current_context('self')
        self.assertIn('contexts', cfg.content)
        self.assertIn('clusters', cfg.content)
        self.assertIn('users', cfg.content)

    def test_merge_items(self):
        cfg = Config.from_params()

        # default item exists
        self.assertEqual(len(cfg.content['users']), 1)

        # updates default with new value
        cfg.set_credentials(None, token='abc123')
        self.assertEqual(len(cfg.content['users']), 1)

        # adds a new item to the list
        cfg.set_credentials('other', token='abc123')
        self.assertEqual(len(cfg.content['users']), 2)

        # duplicate; does nothing
        cfg.set_credentials(None, token='abc123')
        self.assertEqual(len(cfg.content['users']), 2)

        # updates default with new value
        cfg.set_credentials(None, token='abc456')
        self.assertEqual(len(cfg.content['users']), 2)

        # do not erase existing data
        cfg.set_credentials(None)
        self.assertEqual(len(cfg.content['users']), 2)

        auth = None
        for u in cfg.content['users']:
            if u['name'] == 'self':
                auth = u['user']

        self.assertEqual(auth, {'token': 'abc456'})

    def test_set_cluster(self):
        cfg = Config(None)

        cfg.set_cluster('test', server='http://localhost:8080', api_version='v2')

        self.assertEqual(cfg.clusters['test'], {'server': 'http://localhost:8080'})
        self.assertEqual(cfg.content['apiVersion'], 'v2')

        cfg.set_cluster('sample', cert_authority='/tmp/.minikube/ca.crt', embed_certs=True)
        self.assertIsNotNone(cfg.clusters['sample'].get('certificate-authority'))
        self.assertIsNotNone(cfg.clusters['sample'].get('certificate-authority-data'))

    def test_set_credentials(self):
        cfg = Config(None)

        cfg.set_credentials('me', username='admin')
        self.assertEqual(cfg.users['me'], {'username': 'admin'})

        cfg.set_credentials('me', password='admin')
        self.assertEqual(cfg.users['me'], {'username': 'admin', 'password': 'admin'})

        session = cfg.format_session()
        # user is not part of current context
        self.assertFalse(session.get('headers', {}).get('Authorization', '').startswith('Basic '))

        cfg.set_context(None, user='me')
        session = cfg.format_session()
        self.assertTrue(session.get('headers', {}).get('Authorization', '').startswith('Basic '))

        cfg.set_credentials('tester', client_cert='/tmp/.minikube/apiserver.crt',
                            client_key='/tmp/.minikube/apiserver.key', embed_certs=True)

        self.assertIsNotNone(cfg.users['tester'].get('client-certificate'))
        self.assertIsNotNone(cfg.users['tester'].get('client-certificate-data'))
        self.assertIsNotNone(cfg.users['tester'].get('client-key'))
        self.assertIsNotNone(cfg.users['tester'].get('client-key-data'))

    def test_set_context(self):
        cfg = Config(None)

        cfg.set_context(None, user='other', use=True)
        self.assertIsNone(cfg.context.get('user'))

        cfg.set_context(None, namespace='default')
        self.assertEqual(cfg.context.get('namespace'), 'default')


if __name__ == '__main__':
    unittest.main()
