#!/bin/bash

start_k8s() {
  # Note: takes some time for the http server to pop up :)
  # MINIMUM 15 seconds
  echo "
  ##########
  STARTING KUBERNETES
  ##########
  "
  if [ ! -f /usr/bin/kubectl ] && [ ! -f /usr/local/bin/kubectl ]; then
    echo "No kubectl bin exists? Please install."
    return 1
  fi

  # Use alpha for now since this contains the new hyperkube format going forward
  K8S_VERSION=1.3.4
  docker run \
  --volume=/:/rootfs:ro \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:rw \
  --volume=/var/lib/kubelet/:/var/lib/kubelet:rw \
  --volume=/var/run:/var/run:rw \
  --net=host \
  --pid=host \
  --privileged=true \
  -d \
  gcr.io/google_containers/hyperkube-amd64:v${K8S_VERSION} \
  /hyperkube kubelet \
      --containerized \
      --hostname-override="127.0.0.1" \
      --address="0.0.0.0" \
      --api-servers=http://localhost:8080 \
      --config=/etc/kubernetes/manifests \
      --cluster-dns=10.0.0.10 \
      --cluster-domain=cluster.local \
      --allow-privileged=true --v=2


  until curl 127.0.0.1:8080 &>/dev/null;
  do
      echo ...
      sleep 1
  done
}

config_k8s() {
  # Set the appropriate .kube/config configuration
  kubectl config set-cluster dev --server=http://localhost:8080
  kubectl config set-context dev --cluster=dev --user=default
  kubectl config use-context dev
  kubectl config set-credentials default --token=foobar

  # Debug info:
  cat ~/.kube/config

  # Delay due to CI being a bit too slow when first starting k8s
  sleep 5
}


stop_k8s() {
  echo "
  ##########
  STOPPING KUBERNETES
  ##########
  "

  # Delete via image name google_containers
  # Delete all containers started (names start with k8s_)
  # Run twice in-case a container is replicated during that time
  for run in {0..2}
  do
    docker ps -a | grep 'k8s_' | awk '{print $1}' | xargs --no-run-if-empty docker rm -f
    docker ps -a | grep 'gcr.io/google_containers/hyperkube-amd64' | awk '{print $1}' | xargs --no-run-if-empty docker rm -f
  done
}

clean_k8s() {
  # Delete all hanging containers
  echo "\n-----Cleaning / removing all pods and containers from default namespace-----\n"
  kubectl get pvc,pv,svc,rc,po | grep -v 'k8s-\|NAME\|CONTROLLER\|kubernetes' | awk '{print $1}' | xargs --no-run-if-empty kubectl delete pvc,pv,svc,rc,po --grace-period=1 2>/dev/null
}

wait_k8s() {
  echo "Waiting for k8s po/svc/rc to finish terminating..."
  kubectl get po,svc,rc
  sleep 3 # give kubectl chance to catch up to api call
  while [ 1 ]
  do
    k8s=`kubectl get po,svc,rc | grep Terminating`
    if [[ $k8s == "" ]]
    then
      echo "k8s po/svc/rc terminated!"
      break
    else
      echo "..."
    fi
    sleep 1
  done
}


if [[ $1 == "config" ]]; then
  config_k8s 
elif [[ $1 == "clean" ]]; then
  clean_k8s 
elif [[ $1 == "start" ]]; then
  start_k8s
elif [[ $1 == "stop" ]]; then
  stop_k8s
elif [[ $1 == "wait" ]]; then
  wait_k8s
else
  echo $"Usage: kubernetes.sh {config|clean|start|stop|wait}"
fi
