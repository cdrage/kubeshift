class KubeOpenshiftError(Exception):
    pass


class KubeKubernetesError(Exception):
    pass


class KubeConfigError(Exception):
    pass


class KubeClientError(Exception):
    pass


class KubeConnectionError(Exception):
    pass


class KubeBaseError(Exception):
    pass


class ProviderFailedException(Exception):
    pass
