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
    return _get_requirements('requirements.txt')


with open('kubeshift/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')


setup(
    name='kubeshift',
    version=version,
    description='A universal python library for container orchestrators',
    author='cdrage',
    author_email='cdrage@redhat.com',
    url='https://github.com/cdrage/kubeshift',
    license="LGPL3",
    packages=find_packages(),
    install_requires=_install_requirements(),
    keywords=['kubernetes', 'kubeshift', 'openshift', 'docker'],
    classifiers=[]
)
