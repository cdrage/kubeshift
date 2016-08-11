import re

from setuptools import setup, find_packages


def _get_requirements(path):
    try:
        with open(path) as f:
            packages = f.read().splitlines()
    except (IOError, OSError) as ex:
        raise RuntimeError("Can't open file with requirements: %s", repr(ex))
    packages = (p.strip() for p in packages if not re.match("^\s*#", p))
    packages = list(filter(None, packages))
    return packages


def _install_requirements():
    requirements = _get_requirements('requirements.txt')
    return requirements

setup(
    name='kubeshift',
    version='0.0.1',
    description='A universal library for container orchestrators',
    author='cdrage',
    author_email='container-tools@redhat.com',
    url='https://github.com/cdrage/kubeshift',
    license="LGPL3",
    packages=find_packages(),
    install_requires=_install_requirements()
)
