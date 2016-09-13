# Kubeshift
[![Build Status](https://travis-ci.org/cdrage/kubeshift.svg?branch=master)](https://travis-ci.org/cdrage/kubeshift)
[![Coverage Status](https://coveralls.io/repos/github/cdrage/kubeshift/badge.svg?branch=master)](https://coveralls.io/github/cdrage/kubeshift?branch=master)

## Introduction

_Kubeshift_ is a multi-provider Python library for container orchestrators. We connect and communicate with each container orchestator 100% through their TLS (if available) HTTP API.

__Features:__

  - 100% HTTP API
  - Auto-parsing of `~/.kube/config`
  - `.kube/config` generation
  - TLS authentication
  - 100% test coverage with functional and integration tests

## Providers

At the moment we support:

  - Kubernetes
  - OpenShift
  - Mesos (soon!)

## Library installation

#### Pip
```
sudo pip install kubeshift
```

#### Manual / development
```
git clone https://github.com/cdrage/kubeshift && cd kubeshift
make install
```

## Python requirements

```sh
▶ cat requirements.txt 
anymarkup
requests
```

## Methods and examples

#### Configuration import

The configuration file used with the provider must be an _object_. Currently we support the import and generation of Kubernetes and OpenShift configuration files .

```python
import kubeshift

# Import the configuration, this can be either from a file
config = kubeshift.Config.from_file("/home/user/.kube/config")
client = kubeshift.Client(config, "kubernetes")

# Or generated via a set of parameters
config_params = kubeshift.Config.from_params(api="https://localhost:8080", auth="foobar", ca="/home/user/.kube/ca.cert", verify=True)
client = kubeshift.Client(config_params, "kubernetes")
```

#### Implemented methods

**The main methods for each provider are:**
```
.create(object)
.delete(object)
.scale(object)
```

API calls are also available via their corresponding method. Each call returns a dictionary object container all information. These methods are created from the list of calls at `http://localhost:8080/apis`. Some calls *require* namespace to be provided. Otherwise, 'default' will be used.

**API call methods:**
```
.componentstatuses
.namespaces
.nodes
.persistentvolumes
.thirdpartyresources
```

**Namespaced API call methods:**
```
.configmaps(namespace="default")
.endpoints(namespace="default")
.events(namespace="default")
.limitranges(namespace="default")
.persistentvolumeclaims(namespace="default")
.pods(namespace="default")
.podtemplates(namespace="default")
.resourcequotas(namespace="default")
.secrets(namespace="default")
.serviceaccounts(namespace="default")
.services(namespace="default")
.daemonsets(namespace="default")
.deployments(namespace="default")
.horizontalpodautoscalers(namespace="default")
.ingresses(namespace="default")
.jobs(namespace="default")
.networkpolicies(namespace="default")
.replicasets(namespace="default")
.petsets(namespace="default")
.poddisruptionbudgets(namespace="default")
```

**These API calls can further filtered via these methods:**
```
.filter(namespace="foo", status="Running")
.all()
.metadata()
.items()
```

**Full example:**
```python
import kubeshift
import getpass

# Example k8s object
k8s_object = {"apiVersion": "v1", "kind": "Pod", "metadata": {"labels": {"app": "helloapache"}, "name": "helloapache"}, "spec": {
    "containers": [{"image": "nginx", "name": "helloapache", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}

# Client configuration
user = getpass.getuser()
config = kubeshift.Config.from_file("/home/%s/.kube/config" % user)
client = kubeshift.Client(config, "kubernetes")

# Main methods
client.create(k8s_object)  # Creates the k8s object
# client.scale(k8s_object, replicas=3) # Scales the k8s object (if it's a service)
client.delete(k8s_object)  # Deletes the k8s object

# API calls

# Namespaces
client.namespaces()

# Pods
client.pods().all()
client.pods().filter(namespace="default", status="Running")
client.pods().metadata()
client.pods().items()
```
