import kubeshift

a = kubeshift.Client(kubeshift.KubeConfig.from_file("/home/wikus/.kube/config"), "kubernetes")
print a.namespaces()
