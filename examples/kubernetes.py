import kubeshift

a = kubeshift.Client(kubeshift.Config.from_file("/home/wikus/.kube/config"), "kubernetes")
print a.namespaces()
