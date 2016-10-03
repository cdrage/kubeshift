"""Perform API query for any provider with filtering features."""
import six

from kubeshift.constants import DEFAULT_NAMESPACE
from kubeshift.queries import utils


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
        return self.client.request('get', self.url) or {}

    def items(self):
        """Select the list of items from the query results."""
        return self.all().get('items', [])

    def metadata(self):
        """Filter the results to provide only the metadata only."""
        return [s.get('metadata', {}) for s in self.items()]

    def filter(self, status=None):
        """Filter by status.

        :param str status: filter by `status.phace` value
        """
        if status:
            return [s for s in self.items() if s.get('status', {}).get('phase') == status]

        return []

    def by_name(self, name):
        """Fetch resource by name.

        :param str name: name of a resource
        :returns: a resource object
        """
        if not name:
            return {}
        return self.client.request('get', self.url + '/' + name)

    def by_selector(self, selectors):
        """Query resource by labelSelector.

        selector attributes:
            * key: (str) label key/name **REQUIRED**
            * value: (str|list) label value(s)
            * op: (str|None) one of the support operations ['=', '!=', 'in', 'notin'] default `=`

        Exists indicated by not providing `value` or setting `value` to `None`.

        .. warning::

            Missing key or unknown op results in empty list.

        .. note::

            http://kubernetes.io/docs/user-guide/labels/#label-selectors

        :param list selectors: a list of selectors (dict) that filters resources by label(s)
        :returns: list of resources that match selector criteria
        :rtype: list
        """
        qs = utils.selectors_to_qs(selectors)
        if not qs:
            return []
        return self.client.request('get', self.url + qs).get('items', [])


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
