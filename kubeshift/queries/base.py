"""Perform API query for any provider with filtering features."""
import six

from kubeshift.constants import DEFAULT_NAMESPACE


class Query(object):
    """Performs queries with filters."""

    def __init__(self, client, url):
        """
        Use a Provider client and lookup for specific API..

        client [KubeBase]
        """
        self.client = client
        self.url = url

    def all(self):
        """Perform query with no filters (all results)."""
        return self.client.request("get", self.url) or {}

    def items(self):
        """Select the list of items from the query results."""
        return self.all().get('items', [])

    def metadata(self):
        """Filter the results to provide only the metadata only."""
        return [s.get('metadata', {}) for s in self.items()]

    def filter(self, namespace=None, status=None):
        """
        Filter by namespace and/or status.

        Apply one or both filter(s) provided to the query results.
        """
        if namespace and status:
            return [s for s in self.items() if s.get('metadata', {}).get('namespace') == namespace and s.get('status', {}).get('phase') == status]
        elif namespace:
            return [s for s in self.items() if s.get('metadata', {}).get('namespace') == namespace]
        elif status:
            return [s for s in self.items() if s.get('status', {}).get('phase') == status]

        return []


def queryapi(version, kind, nsarg=True):
    """Make Query API.

    .. py:decorator:: queryapi

        Creates a named query api.
    """
    def decorator(func):
        @six.wraps(func)
        def handler(self, namespace=DEFAULT_NAMESPACE):
            if not nsarg:
                namespace = None
            url = self._generate_url(api_version=version,
                                     kind=kind,
                                     namespace=namespace)
            return Query(self, url)
        return handler
    return decorator
