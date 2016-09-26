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


class Config(object):
    """Config manages configuration file with accessor properties."""

    def __init__(self, content, filepath=None):

        self.content = content or copy.deepcopy(DEFAULT_CFG)
        self.filepath = filepath or DEFAULT_FILE
        self.current_context = None

        self.set_current_context(self.content.get('current-context'))
        logger.debug("current context: %s", self.current_context)

    @property
    def clusters(self):
        if not getattr(self, '_clusters', None):
            self._clusters = {}
            for cr in self.content.get('clusters', []):
                self._clusters[cr['name']] = copy.deepcopy(cr['cluster'])
        return self._clusters

    @property
    def users(self):
        if not getattr(self, '_users', None):
            self._users = {}
            for ur in self.content.get('users', []):
                self._users[ur['name']] = copy.deepcopy(ur['user'])
        return self._users

    @property
    def contexts(self):
        if not getattr(self, '_contexts', None):
            self._contexts = {}
            for cr in self.content.get('contexts', []):
                self._contexts[cr['name']] = copy.deepcopy(cr['context'])
        return self._contexts

    @property
    def context(self):
        return self.contexts.get(self.current_context, {})

    @property
    def cluster(self):
        return self.clusters.get(self.context.get('cluster', ''), {})

    @property
    def user(self):
        return self.users.get(self.context.get('user', ''), {})

    def set_current_context(self, ctx_key):
        if not ctx_key and len(self.contexts) == 1:
            ctx_key = list(self.contexts.keys())[0]

        if self.current_context == ctx_key:
            # already set
            return

        if ctx_key not in self.contexts:
            # context does not exist
            return

        self.content['current-context'] = self.current_context = ctx_key

    def _add(self, group, subgroup, data, name):
        if group not in self.content:
            self.content[group] = []

        if not name:
            name = DEFAULT_NAME

        found = False
        for idx, item in enumerate(self.content[group]):
            if item['name'] == name:
                found = True
                if item[subgroup] == data:
                    # duplicate; stop checking
                    break

                if item[subgroup] and not data:
                    # avoid reseting or wiping away existing data
                    break

                # not a duplicate name and value, but the name exists
                # so update the existing value with new value.
                self.content[group][idx][subgroup] = data

                # reset the flattened property
                setattr(self, '_' + group, {})
                break

        if not found:
            # not found previously so add a new item to the list
            self.content[group].append(
                {
                    'name': name,
                    subgroup: data
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

    def _certfile(self, key, data):
        # As per github.com/kubernetes/kubernetes/blob/master/pkg/client/unversioned/clientcmd/api/v1/types.go#L67
        # -data contains PEM-encoded data and overrides certificate-authority

        data_key = '{}-data'.format(key)
        if data_key in data and data[data_key]:
            with tempfile.NamedTemporaryFile(delete=False) as f:
                f.write(base64.b64decode(data[data_key]))
            return f.name

        # check if already a file
        if key in data and os.path.isfile(data[key]):
            return data[key]

        return None

    def format_session(self):
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

        ca = self._certfile('certificate-authority', cluster)
        if ca:
            session['verify'] = ca

        if cluster.get('insecure-skip-tls-verify', False):
            session['verify'] = False

        if cluster.get('server', '').startswith('http://'):
            session['verify'] = False

        # read the user to handle setting user auth
        user = self.user

        cert = self._certfile('client-certificate', user)
        key = self._certfile('client-key', user)
        if cert and key:
            session['cert'] = (cert, key)

        if 'token' in user:
            session['headers']['Authorization'] = 'Bearer {}'.format(user['token'])

        return session

    def set_user_auth(self, auth, name=None):
        user = {}

        if auth:
            if isinstance(auth, dict):
                if auth.get('client-certificate'):
                    user['client-certificate'] = auth.get('client-certificate')
                if auth.get('client-key'):
                    user['client-key'] = auth.get('client-key')
            else:
                user['token'] = auth

        self._add_user(user, name)

    def write_file(self):
        config_path_dir = os.path.dirname(self.filepath)
        if not os.path.exists(config_path_dir):
            os.makedirs(config_path_dir)

        yaml.dump(self.content, open(self.filepath, 'w'))

    @classmethod
    def from_file(cls, filepath):
        """Load a file using anymarkup.

        Params:
            filepath (str): File location

        Returns:
            Config(obj): An object representing the contents of file

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

        Params:
            api(str): API URL of the server
            auth(str|dict): Authentication key for the server
            ca(str): The certificate being used. This can be either a file location or a base64 encoded string
            verify(bool): true/false of whether or not certificate verification is enabled
            filepath(str): File location

        Returns:
            config(obj): An object file of generate .kube/config

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

        cfg._add_context({'cluster': cluster_name, 'user': user_name}, context_name)
        cfg.set_current_context(context_name)

        cluster = {}

        if api:
            cluster['server'] = api

        if ca:
            cluster['certificate-authority'] = ca

        if verify is False:
            cluster['insecure-skip-tls-verify'] = True

        cfg._add_cluster(cluster, cluster_name)

        cfg.set_user_auth(auth, user_name)

        return cfg
