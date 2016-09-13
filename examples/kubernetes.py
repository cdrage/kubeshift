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
