#!/bin/bash

start_openshift() {
  hash minishift 2>/dev/null || { echo "No minishift bin exists? Please install."; return 1; }
  hash oc 2>/dev/null || { echo "No oc bin exists? Please install."; return 1; }

  minishift start

  oc login -u admin -p admin

  oc new-project foo || oc project foo
}

stop_openshift() {

  minishift stop
}

if [[ $1 == "start" ]]; then
  start_openshift
elif [[ $1 == "stop" ]]; then
  stop_openshift
else
  echo $"Usage: openshift.sh {start|stop}"
fi
