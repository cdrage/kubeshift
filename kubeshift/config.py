"""Kube Config handles the parsing and writing of config file."""
import base64
import copy
import logging
import os
import tempfile

import yaml

from kubeshift.constants import LOGGER_DEFAULT

logger = logging.getLogger(LOGGER_DEFAULT)

DEFAULT_FILE = os.path.expanduser(os.path.join('~', '.kube', 'config'))
DEFAULT_NAME = 'self'
DEFAULT_CFG = {
    'apiVersion': 'v1',
    'kind': 'Config',
    'current-context': None,
    'preferences': {},
    'clusters': [],
    'contexts': [],
    'users': [],
}


def _basic_auth_str(username, password):
    auth = base64.b64encode(('%s:%s' % (username, password)).encode('latin1')).strip()
    if not isinstance(auth, str):
        auth = auth.decode('ascii')
    return 'Basic ' + auth


def _encode(filepath):
    with open(filepath, 'rb') as fd:
        return base64.b64encode(fd.read())


def _decode(content):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(base64.b64decode(content))
    return f.name


def _certfile(key, data):
    # As per github.com/kubernetes/kubernetes/blob/master/pkg/client/unversioned/clientcmd/api/v1/types.go#L67
    # -data contains PEM-encoded data and overrides certificate-authority

    data_key = '{}-data'.format(key)
    if data_key in data and data[data_key]:
        return _decode(data[data_key])

    # check if already a file
    if key in data and os.path.isfile(data[key]):
        return data[key]

    return None


class Config(object):
    """Config manages configuration file with accessor properties."""

    def __init__(self, content, filepath=None):
        """Constructor.

        :param dict content: parsed content of kubeconfig file
        :param str filepath: path to kubeconfig file (default: $HOME/.kube/config)

        """
        self.content = content or copy.deepcopy(DEFAULT_CFG)
        self.filepath = filepath or DEFAULT_FILE
        self.current_context = None

        self.set_current_context(self.content.get('current-context'))
        logger.debug("current context: %s", self.current_context)

    @property
    def clusters(self):
        """Return flattened clusters keyed by cluster name."""
        if not getattr(self, '_clusters', None):
            self._clusters = {}
            for cr in self.content.get('clusters', []):
                self._clusters[cr['name']] = copy.deepcopy(cr['cluster'])
        return self._clusters

    @property
    def users(self):
        """Return flattened users keyed by user name."""
        if not getattr(self, '_users', None):
            self._users = {}
            for ur in self.content.get('users', []):
                self._users[ur['name']] = copy.deepcopy(ur['user'])
        return self._users

    @property
    def contexts(self):
        """Return flattened contexts keyed by context name."""
        if not getattr(self, '_contexts', None):
            self._contexts = {}
            for cr in self.content.get('contexts', []):
                self._contexts[cr['name']] = copy.deepcopy(cr['context'])
        return self._contexts

    @property
    def context(self):
        """Return context entry referenced by current-context."""
        return self.contexts.get(self.current_context, {})

    @property
    def cluster(self):
        """Return cluster entry referenced by current-context."""
        return self.clusters.get(self.context.get('cluster', ''), {})

    @property
    def user(self):
        """Return user entry referenced by current-context."""
        return self.users.get(self.context.get('user', ''), {})

    def set_current_context(self, ctx_key):
        """Set the current-context in a kubeconfig file.

        :param str ctx_key: name of the context to use as the current-context
        """
        if not ctx_key and len(self.contexts) == 1:
            ctx_key = list(self.contexts.keys())[0]

        if self.current_context == ctx_key:
            # already set
            return

        if ctx_key not in self.contexts:
            # context does not exist
            return

        self.content['current-context'] = self.current_context = ctx_key

    def set_cluster(self, name, server=None, cert_authority=None, embed_certs=False,
                    skip_verify=False, api_version=None):
        """Set a cluster entry in kubeconfig.

        Specifying a name that already exists will merge new fields on top of existing
        values for those fields.

        :param str name: name of cluster entry
        :param str server: server for the cluster entry in kubeconfig
        :param str cert_authority: path to certificate-authority file for the cluster entry in kubeconfig
        :param bool embed_certs: embed-certs for the cluster entry in kubeconfig (default: False)
        :param bool skip_verify: insecure-skip-tls-verify for the cluster entry in kubeconfig (default: False)
        :param str api_version: api-version for the cluster entry in kubeconfig
        """
        if api_version:
            self.content['apiVersion'] = api_version

        data = {}

        if server:
            data['server'] = server

        if cert_authority and os.path.exists(cert_authority):
            if embed_certs:
                data['certificate-authority-data'] = _encode(cert_authority)
            data['certificate-authority'] = cert_authority

        if skip_verify:
            data['insecure-skip-tls-verify'] = True

        self._add_cluster(data, name)

    def set_credentials(self, name, token=None, username=None, password=None,
                        client_cert=None, client_key=None, embed_certs=False):
        """Set a user entry in kubeconfig.

        Specifying a name that already exists will merge new fields on top of existing values.

        :param str name: name of user entry
        :param str token: token for the user entry in kubeconfig (ex. Bearer token)
        :param str username: username for the user entry in kubeconfig
        :param str password: password for the user entry in kubeconfig
        :param str client_cert: path to client-certificate file for the user entry in kubeconfig
        :param str client_key: path to client-key file for the user entry in kubeconfig
        :param bool embed_certs: embed client cert/key for the user entry in kubeconfig (default: False)
        """
        data = {}

        if token:
            data['token'] = token

        if username:
            data['username'] = username

        if password:
            data['password'] = password

        if client_cert and os.path.exists(client_cert):
            if embed_certs:
                data['client-certificate-data'] = _encode(client_cert)
            data['client-certificate'] = client_cert

        if client_key and os.path.exists(client_key):
            if embed_certs:
                data['client-key-data'] = _encode(client_key)
            data['client-key'] = client_key

        self._add_user(data, name)

    def set_context(self, name, cluster=None, user=None, namespace=None, use=False):
        """Set a context entry in kubeconfig.

        Specifying a name that already exists will merge new fields on top of
        existing values for those fields.

        :param str name: name of context cluster
        :param str cluster: cluster for the context entry in kubeconfig
        :param str user: user for the context entry in kubeconfig
        :param str namespace: namespace for the context entry in kubeconfig
        :param bool use: set the context as current context
        """
        data = {}

        if cluster and cluster in self.clusters:
            data['cluster'] = cluster

        if user and user in self.users:
            data['user'] = user

        if namespace:
            data['namespace'] = namespace

        self._add_context(data, name)

        if use:
            self.set_current_context(name)

    def _add(self, group, subgroup, data, name):
        if group not in self.content:
            self.content[group] = []

        if not name:
            name = DEFAULT_NAME

        found = False
        for idx, item in enumerate(self.content[group]):
            if item['name'] == name:
                found = True
                self.content[group][idx][subgroup].update(data or {})

                # reset the flattened property
                setattr(self, '_' + group, {})
                break

        if not found:
            # not found previously so add a new item to the list
            self.content[group].append(
                {
                    'name': name,
                    subgroup: data or {}
                }
            )
            # reset the flattened property
            setattr(self, '_' + group, {})

    def _add_context(self, context, name=None):
        self._add('contexts', 'context', context, name)

    def _add_cluster(self, cluster, name=None):
        self._add('clusters', 'cluster', cluster, name)

    def _add_user(self, user, name=None):
        self._add('users', 'user', user, name)

    def format_session(self):
        """Format content from current-context as a request session."""
        session = {
            'cert': None,
            'headers': {},
            'verify': True
        }

        # if the current context is not set but there is only
        # one context available then set the current_context to
        # the only context available.
        self.set_current_context(None)

        # no session specified and there is not just a single
        # context to select from.
        if not self.current_context:
            return session

        # read the cluster to handle setting the server SSL settings
        cluster = self.cluster

        ca = _certfile('certificate-authority', cluster)
        if ca:
            session['verify'] = ca

        if cluster.get('insecure-skip-tls-verify', False):
            session['verify'] = False

        if cluster.get('server', '').startswith('http://'):
            session['verify'] = False

        # read the user to handle setting user auth
        user = self.user

        cert = _certfile('client-certificate', user)
        key = _certfile('client-key', user)
        if cert and key:
            session['cert'] = (cert, key)

        if user.get('token'):
            session['headers']['Authorization'] = 'Bearer {}'.format(user['token'])
        elif user.get('username') and user.get('password'):
            session['headers']['Authorization'] = _basic_auth_str(user['username'],
                                                                  user['password'])

        return session

    def write_file(self):
        """Save kubeconfig content to disk."""
        config_path_dir = os.path.dirname(self.filepath)
        if not os.path.exists(config_path_dir):
            os.makedirs(config_path_dir)

        yaml.dump(self.content, open(self.filepath, 'w'))

    @classmethod
    def from_file(cls, filepath):
        """Load a file from disk.

        :param str filepath: File location
        :returns: A Config instance representing the .kube/config file
        :rtype: :py:class:`~kubeshift.config.Config`
        """
        if not filepath:
            filepath = DEFAULT_FILE
        if not os.path.isfile(filepath):
            return cls(None, filepath)

        logger.debug("Parsing %s", filepath)

        with open(filepath) as f:
            content = yaml.safe_load(f.read())
        return cls(content, filepath)

    @classmethod
    def from_params(cls, context_name=None, api=None, username=None, auth=None,
                    ca=None, verify=True, filepath=None):
        """
        Create a .kube/config configuration as an object based upon the arguments given.

        :param str context_name: name of context to use for current-context
        :param str api: API URL of the server
        :param str username: name of user entry
        :param str|dict auth: Authentication key for the server
        :param str ca: file location ca certificate for server
        :param bool verify: true/false of whether or not certificate verification is enabled
        :param str filepath: kubeconfig file location to use or as to be saved to
        :returns: A Config instance representing the .kube/config file
        :rtype: :py:class:`~kubeshift.config.Config`
        """
        cfg = cls.from_file(filepath)

        if context_name:
            cfg.set_current_context(context_name)
            cluster_name = cfg.context.get('cluster', DEFAULT_NAME)
            user_name = cfg.context.get('user', username or DEFAULT_NAME)
        else:
            context_name = DEFAULT_NAME
            cluster_name = DEFAULT_NAME
            user_name = username or DEFAULT_NAME

        cfg.set_cluster(cluster_name, server=api, cert_authority=ca, skip_verify=not verify)

        cfg.set_credentials(user_name)
        if auth:
            if isinstance(auth, dict):
                cfg.set_credentials(user_name, client_cert=auth.get('client-certificate'),
                                    client_key=auth.get('client-key'))
            else:
                cfg.set_credentials(user_name, token=auth)

        cfg.set_context(context_name, cluster=cluster_name, user=user_name, use=True)

        return cfg
