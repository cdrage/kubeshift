# Kubeshift
[![Build Status](https://travis-ci.org/cdrage/kubeshift.svg?branch=master)](https://travis-ci.org/cdrage/kubeshift)
[![Coverage Status](https://coveralls.io/repos/cdrage/kubeshift/badge.svg?branch=master&service=github)](https://coveralls.io/github/cdrage/kubeshift?branch=master)

## Introduction

_Kubeshift_ is a multi-provider Python library for container orchestrators. We connect and communicate with each container orchestator 100% through their TLS (if available) HTTP API.

__Features:__

  - 100% HTTP API
  - Auto-parsing of `~/.kube/config`
  - TLS/Websocket authentication
  - High test coverage

## Providers

At the moment we support:

  - Kubernetes
  - OpenShift
  - Mesos (soon!)

## Installation

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

## Examples

```python
import kubeshift

a = kubeshift.Client(kubeshift.Config.from_file("/home/user/.kube/config"), "kubernetes")
a.namespaces()
```
