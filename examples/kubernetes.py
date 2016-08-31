import getpass
import kubeshift

user = getpass.getuser()

a = kubeshift.Client(kubeshift.Config.from_file("/home/%s/.kube/config" % user), "kubernetes")
print a.namespaces()
