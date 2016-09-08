import getpass
import kubeshift

user = getpass.getuser()

client = kubeshift.Client(kubeshift.Config.from_file("/home/%s/.kube/config" % user), "kubernetes")

# Print out all available namespaces
print client.namespaces()

k8s_object = {"apiVersion": "v1", "kind": "Pod", "metadata": {"labels": {"app": "hellonginx"}, "name": "hellonginx"}, "spec": {"containers": [{"image": "nginx", "name": "hellonginx", "ports": [{"containerPort": 80, "hostPort": 80, "protocol": "TCP"}]}]}}

# Create the object
client.create(k8s_object)

# Delete the object
# client.delete(k8s_object)
