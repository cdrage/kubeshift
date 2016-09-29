"""Kubeshift is a multi-provider Python library for Kubernetes (kube) and Openshift (shift)."""
import logging

from kubeshift.config import Config  # noqa
from kubeshift.kubernetes import KubernetesClient  # noqa
from kubeshift.openshift import OpenshiftClient  # noqa

logging.getLogger().addHandler(logging.NullHandler())

__title__ = 'kubeshift'
__version__ = '0.0.4'
__author__ = 'cdrage'
__license__ = 'LGPL3'
