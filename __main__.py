from pulumi.provider.experimental import component_provider_host
from gke_kubeconfig import GKEKubeconfig

if __name__ == "__main__":
    component_provider_host(name="gke-kubeconfig-component", components=[GKEKubeconfig])
