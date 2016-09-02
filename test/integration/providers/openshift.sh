#!/bin/bash

start_openshift() {
  # Start up Dockerized version of OpenShift Origin
  # Note: takes some time for the http server to pop up :)
  # MINIMUM 15 seconds
  echo "
  ##########
  STARTING OPENSHIFT 
  ##########
  "
  if [ ! -f /usr/bin/kubectl ] && [ ! -f /usr/local/bin/kubectl ]; then
    echo "No kubectl bin exists? Please install."
    return 1
  fi

  docker rm -f origin
  docker run -d --name "origin" \
    --privileged --pid=host --net=host \
    -v /:/rootfs:ro -v /var/run:/var/run:rw -v /sys:/sys -v /var/lib/docker:/var/lib/docker:rw \
    -v /var/lib/origin/openshift.local.volumes:/var/lib/origin/openshift.local.volumes \
    openshift/origin start

  until curl 127.0.0.1:8443 &>/dev/null;
  do
      echo ...
      sleep 1
  done
}

stop_openshift() {
  echo "
  ##########
  STOPPING OPENSHIFT 
  ##########
  "
  docker rm -f origin

  # Remove all kubernetes back-end containers created by origin
  # Ran twice due to Debian aufs "busy" driver issue
  for run in {0..2}
  do
    docker ps -a | grep 'gcr.io/google_containers/hyperkube' | awk '{print $1}' | xargs --no-run-if-empty docker rm -f
    docker ps -a | grep 'gcr.io/google_containers/etcd' | awk '{print $1}' | xargs --no-run-if-empty docker rm -f
    docker ps -a | grep 'k8s_' | awk '{print $1}' | xargs --no-run-if-empty docker rm -f || true
  done
}

config_openshift() {
  echo "
  ##########
  SETTING UP OC CONFIGURATION
  ##########
  "

  # Retrieve the API key to use
  API_KEY=`curl -k -L -D - -u openshift:openshift -H 'X-CSRF-Token: 1' 'https://localhost:8443/oauth/authorize?response_type=token&client_id=openshift-challenging-client' 2>&1 | grep -oP "access_token=\K[^&]*"`
  echo $API_KEY

  oc config set-credentials openshift --token=$API_KEY
  oc config set-cluster openshift1 --server=https://localhost:8443 --insecure-skip-tls-verify=true
  oc config set-context openshift --cluster=openshift1 --user=openshift
  oc config use-context openshift
  oc config set contexts.openshift.namespace foo

  oc new-project foo
}

# Use docker openshift container to get oc (assuming host doesn't have it)
wait_openshift() {
  echo "Waiting for oc po/svc/rc to finish terminating..."
  docker exec -it origin oc get po,svc,rc
  sleep 3 # give kubectl chance to catch up to api call
  while [ 1 ]
  do
    oc=`docker exec -it origin oc get po,svc,rc | grep Terminating`
    if [[ $oc == "" ]]
    then
      echo "oc po/svc/rc terminated!"
      break
    else
      echo "..."
    fi
    sleep 1
  done
}

if [[ $1 == "config" ]]; then
  config_openshift
elif [[ $1 == "start" ]]; then
  start_openshift
elif [[ $1 == "stop" ]]; then
  stop_openshift
elif [[ $1 == "wait" ]]; then
  wait_openshift
else
  echo $"Usage: openshift.sh {config|start|stop|wait}"
fi
