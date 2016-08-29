# Kubeshift
[![Build Status](https://travis-ci.org/cdrage/kubeshift.svg?branch=master)](https://travis-ci.org/cdrage/kubeshift)
[![Coverage Status](https://coveralls.io/repos/github/cdrage/kubeshift/badge.svg?branch=master)](https://coveralls.io/github/cdrage/kubeshift?branch=master)

## Introduction

_Kubeshift_ is a multi-provider Python library for container orchestrators. We connect and communicate with each container orchestator 100% through their TLS (if available) HTTP API.

__Features:__

  - 100% HTTP API
  - Auto-parsing of `~/.kube/config`
  - `.kube/config` generation
  - TLS/Websocket authentication
  - High test coverage

## Providers

At the moment we support:

  - Kubernetes
  - OpenShift
  - Mesos (soon!)

## Library installation

```
git clone https://github.com/cdrage/kubeshift && cd kubeshift
make install
```

## Python requirements

```
anymarkup
jsonpointer
requests
websocket-client
```

```
pip install -r requirements.txt
```

## Methods and examples

#### Configuration import

The configuration file used with the provider must be an _object_. Currently we support the import and generation of Kubernetes and OpenShift configuration files .

```python
import kubeshift

# Import the configuration, this can be either from file
config = kubeshift.Config.from_file("/home/user/.kube/config")

# Or generated via a set of parameters
config_params = kubeshift.Config.from_params(api="https://localhost:8080", auth="foobar", ca="/home/user/.kube/ca.cert", verify=True)

a = kubeshift.Client(config, "kubernetes")
a.namespaces()
```

#### Implemented methods

The current methods implement for each provider are:
  - .namespaces()
  - .create(object)
  - .delete(object)

```python
import kubeshift

config = kubeshift.Config.from_file("/home/user/.kube/config")

a = kubeshift.Client(config, "kubernetes")

a.namespaces() # Returns a dict of all available namespaces

k8s_object = {"apiVersion": "v1", "kind": "Pod", "metadata": {"labels": {"app": "helloapache"}, "name": "helloapache"}, "spec": {"containers": [{"image": "$image", "name": "helloapache", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}

a.create(k8s_object) # Creates the k8s object

a.delete(k8s_object) # Deletes the k8s object
```

## TODO

 - Upload to pypi
 - 0.0.1 release
 - Better documentation
 - Additional providers other than Kubernetes and OpenShift
 - Simpler import-from-kube-config-file functionality
 - Certificate data fixes
