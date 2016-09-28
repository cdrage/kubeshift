#!/bin/bash

TRAVIS=${TRAVIS:-false}

start_travis_k8s() {
  echo "
  ##########
  STARTING KUBERNETES
  ##########
  "

  hash kubectl 2>/dev/null || { echo "No kubectl bin exists? Please install."; return 1; }

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

  # Set the appropriate .kube/config configuration
  kubectl config set-cluster dev --server=http://localhost:8080
  kubectl config set-context dev --cluster=dev --user=default
  kubectl config use-context dev
  kubectl config set-credentials default --token=foobar

  # Debug info:
  cat ~/.kube/config || :

  # Delay due to CI being a bit too slow when first starting k8s
  # TODO: This needs to be more dynamic instead of just waiting 30 seconds...
  # Could result in false-positives depending on k8s speed on start-up
  sleep 30

}

start_local_k8s() {
  hash minikube 2>/dev/null || { echo "No minikube bin exists? Please install."; return 1; }
  hash kubectl 2>/dev/null || { echo "No kubectl bin exists? Please install."; return 1; }

  minikube start

  kubectl config use-context minikube

  kubectl proxy --port=8080 &
  echo $! > /tmp/kubectl-proxy.pid
}

start_k8s() {
  if [[ "${TRAVIS}" == *"true"* ]]
  then
    start_travis_k8s
  else
    start_local_k8s
  fi
}

stop_travis_k8s() {
  echo "
  ##########
  STOPPING KUBERNETES
  ##########
  "

  # Delete all hanging containers
  echo -e "\n-----Cleaning / removing all pods and containers from default namespace-----\n"
  kubectl get pvc,pv,svc,rc,po | grep -v 'k8s-\|NAME\|CONTROLLER\|kubernetes' | awk '{print $1}' | xargs --no-run-if-empty kubectl delete pvc,pv,svc,rc,po --grace-period=1 2>/dev/null

  echo "Waiting for k8s po/svc/rc to finish terminating..."
  kubectl get po,svc,rc
  sleep 3 # give kubectl chance to catch up to api call
  while 'true'
  do
    k8s=$(kubectl get po,svc,rc | grep Terminating)
    if [[ $k8s == "" ]]
    then
      echo "k8s po/svc/rc terminated!"
      break
    else
      echo "..."
    fi
    sleep 1
  done

  # Delete via image name google_containers
  # Delete all containers started (names start with k8s_)
  # Run twice in-case a container is replicated during that time
  for _ in {0..2}
  do
    docker ps -a | grep 'k8s_' | awk '{print $1}' | xargs --no-run-if-empty docker rm -f
    docker ps -a | grep 'gcr.io/google_containers/hyperkube-amd64' | awk '{print $1}' | xargs --no-run-if-empty docker rm -f
  done
}

stop_local_k8s() {
  pid=$(cat /tmp/kubectl-proxy.pid)
  kill "$pid" && rm /tmp/kubectl-proxy.pid

  minikube stop
}

stop_k8s() {
  if [[ "${TRAVIS}" == *"true"* ]]
  then
    stop_travis_k8s
  else
    stop_local_k8s
  fi
}

if [[ $1 == "start" ]]; then
  start_k8s
elif [[ $1 == "stop" ]]; then
  stop_k8s
else
  echo $"Usage: kubernetes.sh {start|stop}"
fi
