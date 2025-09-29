from typing import Optional, TypedDict, TypeVar

import pulumi
from pulumi import ResourceOptions

T = TypeVar("T")


class GKEKubeconfigArgs(TypedDict):
    cluster_name: pulumi.Input[str]
    """The name of the GKE cluster (`name` field in the `google_container_cluster` resource)"""

    cluster_endpoint: pulumi.Input[str]
    """The URL endpoint of the GKE cluster (`endpoint` field in the `google_container_cluster` resource)"""

    cluster_ca_certificate: pulumi.Input[str]
    """The CA certificate of the GKE cluster (`master_auth["cluster_ca_certificate"]` field in the `google_container_cluster` resource)"""


class GKEKubeconfig(pulumi.ComponentResource):
    """
    Provides a component resource for managing GKE cluster kubeconfig.

    This class generates the kubeconfig for a GKE (Google Kubernetes Engine) cluster.
    It allows external entities to interact with the Kubernetes API using the generated
    kubeconfig. It validates required arguments during initialization and constructs
    the kubeconfig based on the cluster's details provided.
    """

    kubeconfig: pulumi.Output[str]
    """The kubeconfig of the GKE cluster"""

    def __init__(self,
                 name: str,
                 args: GKEKubeconfigArgs,
                 opts: Optional[ResourceOptions] = None) -> None:
        super().__init__('gke-kubeconfig-component:index:GKEKubeconfig', name, {}, opts)

        # Validate required arguments
        required_args = ["cluster_name", "cluster_endpoint", "cluster_ca_certificate"]
        missing_args = []

        for arg_name in required_args:
            if arg_name not in args or args[arg_name] is None:
                missing_args.append(arg_name)

        if missing_args:
            missing_args_str = ", ".join(missing_args)
            raise ValueError(f"Missing required arguments for GKEKubeconfig: {missing_args_str}. "
                             f"All of the following arguments are required: {', '.join(required_args)}")

        name = args["cluster_name"]
        endpoint = args["cluster_endpoint"]
        cluster_ca_certificate = args["cluster_ca_certificate"]

        self.kubeconfig = pulumi.Output.format(
            """
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: {2}
    server: https://{1}
  name: {0}
contexts:
- context:
    cluster: {0}
    user: {0}
  name: {0}
current-context: {0}
kind: Config
preferences: {{}}
users:
- name: {0}
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1beta1
      command: gke-gcloud-auth-plugin
      env: null
      installHint: Install gke-gcloud-auth-plugin for use with kubectl by following
        https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke
      interactiveMode: IfAvailable
      provideClusterInfo: true
            """,
            name,
            endpoint,
            cluster_ca_certificate)

        self.register_outputs({
            "kubeconfig": self.kubeconfig
        })
