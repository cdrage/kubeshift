import kubeshift

a = kubeshift.Client(kubeshift.Config.from_file("/home/user/.kube/config"), "kubernetes")
a.namespaces()
