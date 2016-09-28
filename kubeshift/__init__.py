import logging

from kubeshift.config import Config  # noqa
from kubeshift.kubernetes import KubernetesClient  # noqa
from kubeshift.openshift import OpenshiftClient  # noqa

logging.getLogger().addHandler(logging.NullHandler())
