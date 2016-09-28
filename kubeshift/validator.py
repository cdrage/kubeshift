"""Validate Common object attributes."""
import re

from kubeshift.exceptions import KubeShiftError


def validate(obj):
    """Verify the object has the require attributes.

    Args:
        obj: an instance of a kubernetes / openshift types.

    Returns:
        tuple: api_version, kind, name

    Raises:
        KubeShiftError: if any of the attributes are missing

    """
    if not obj or not isinstance(obj, dict):
        raise KubeShiftError('Resource object missing or incorrect type')

    api_version = obj.get('apiVersion')
    if api_version is None:
        raise KubeShiftError('Resource object missing apiVersion')

    kind = obj.get('kind')
    if kind is None:
        raise KubeShiftError('Resource object missing kind')

    name = obj.get('metadata', {}).get('name')
    if name is None:
        raise KubeShiftError('Resource object missing metadata.name')

    return (api_version, kind, name)


def check_url(url):
    """Verify URL is properly constructed."""
    if not re.match('(?:http|https)://', url):
        raise KubeShiftError('URL does not include HTTP or HTTPS')
