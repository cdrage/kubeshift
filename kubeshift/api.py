import re
from urlparse import urljoin


class Api(object):

    def __init__(self, client, base_url, version, endpoint, namespace=None):
        '''
        Takes in a client connection end-point

        client [KubeBase]
        '''
        self.client = client

        # Check if "v1" is available or any other future versions of the API
        if re.match('v[0-9]|V[0-9]', version):
            base_url = urljoin(base_url, "api/%s" % version)
        else:
            base_url = urljoin(base_url, "apis/")

        versioned_url = urljoin(base_url, version + '/')
        if namespace:
            versioned_url = urljoin(versioned_url, "namespaces/%s/" % namespace)

        self.url = urljoin(versioned_url, endpoint)

    def all(self):
        return self.client.request("get", self.url)

    # TODO: Error if "metadata" isn't available / not there for some reason
    def metadata(self):
        return [s['metadata'] for s in self.items()]

    # TODO: Error if "items" isn't available / not there for some reason
    def items(self):
        return self.client.request("get", self.url)['items']

    def filter(self, namespace=None, status=None):
        if namespace and status:
            return [s for s in self.items() if s['metadata']['namespace'] == namespace and s['status']['phase'] == status]
        elif namespace:
            return [s for s in self.items() if s['metadata']['namespace'] == namespace]
        elif status:
            return [s for s in self.items() if s['status']['phase'] == status]
