# GKE Kubeconfig Pulumi Component

A Pulumi component resource for generating kubeconfig files for Google Kubernetes Engine (GKE) clusters. This component simplifies the process of creating properly configured kubeconfig files that can be used to interact with GKE clusters using kubectl and other Kubernetes tools.

## Features

- Generates valid kubeconfig YAML for GKE clusters
- Uses `gke-gcloud-auth-plugin` for authentication
- Validates required cluster configuration parameters
- Integrates seamlessly with Pulumi infrastructure as code workflows
- Supports Pulumi's component resource model for reusability

## Prerequisites

- Python 3.7+
- Pulumi CLI installed
- Google Cloud SDK (`gcloud`) installed
- `gke-gcloud-auth-plugin` installed (for kubectl authentication)

### Installing gke-gcloud-auth-plugin

```bash
gcloud components install gke-gcloud-auth-plugin
```

For more information, see the [official documentation](https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke).

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. The component can be used directly in your Pulumi Python programs.

## Usage

### Basic Usage

```python
import pulumi
from gke_kubeconfig import GKEKubeconfig, GKEKubeconfigArgs

# Assuming you have a GKE cluster created
cluster_name = "my-gke-cluster"
cluster_endpoint = "https://34.123.45.67"  # Your cluster endpoint
cluster_master_auth = {
    "cluster_ca_certificate": "LS0tLS1CRUdJTi..."  # Base64 encoded CA certificate
}

# Create the kubeconfig component
kubeconfig = GKEKubeconfig(
    "my-cluster-kubeconfig",
    GKEKubeconfigArgs(
        cluster_name=cluster_name,
        cluster_endpoint=cluster_endpoint,
        cluster_master_auth=cluster_master_auth
    )
)

# Export the kubeconfig
pulumi.export("kubeconfig", kubeconfig.kubeconfig)
```

### Integration with GKE Cluster Creation

```python
import pulumi
import pulumi_gcp as gcp
from gke_kubeconfig import GKEKubeconfig, GKEKubeconfigArgs

# Create a GKE cluster
cluster = gcp.container.Cluster(
    "example-cluster",
    location="us-central1",
    initial_node_count=1,
    node_config=gcp.container.ClusterNodeConfigArgs(
        machine_type="e2-medium",
    ),
)

# Generate kubeconfig for the cluster
kubeconfig = GKEKubeconfig(
    "cluster-kubeconfig",
    GKEKubeconfigArgs(
        cluster_name=cluster.name,
        cluster_endpoint=cluster.endpoint,
        cluster_master_auth=cluster.master_auth
    )
)

# Export both cluster info and kubeconfig
pulumi.export("cluster_name", cluster.name)
pulumi.export("cluster_endpoint", cluster.endpoint)
pulumi.export("kubeconfig", kubeconfig.kubeconfig)
```

### Saving Kubeconfig to File

```python
import pulumi
from gke_kubeconfig import GKEKubeconfig, GKEKubeconfigArgs

kubeconfig = GKEKubeconfig("my-kubeconfig", args)

# Save kubeconfig to a local file
kubeconfig.kubeconfig.apply(
    lambda config: open("kubeconfig.yaml", "w").write(config)
)
```

## API Reference

### GKEKubeconfigArgs

The arguments required to create a GKEKubeconfig component.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `cluster_name` | `pulumi.Input[str]` | Yes | The name of the GKE cluster |
| `cluster_endpoint` | `pulumi.Input[str]` | Yes | The URL endpoint of the GKE cluster |
| `cluster_master_auth` | `pulumi.Input[str]` | Yes | The master auth configuration, including the CA certificate of the GKE cluster |

### GKEKubeconfig

The main component resource class.

#### Properties

- `kubeconfig: pulumi.Output[str]` - The generated kubeconfig YAML as a string

#### Methods

- `__init__(name: str, args: GKEKubeconfigArgs, opts: Optional[ResourceOptions] = None)` - Creates a new GKEKubeconfig component

## Generated Kubeconfig Structure

The component generates a kubeconfig with the following structure:

- **API Version**: `v1`
- **Clusters**: Contains the cluster configuration with CA certificate and server endpoint
- **Contexts**: Defines the context linking cluster and user
- **Users**: Configures authentication using `gke-gcloud-auth-plugin`
- **Current Context**: Set to the cluster name

The generated kubeconfig uses the `gke-gcloud-auth-plugin` for authentication, which automatically handles token refresh and authentication with Google Cloud.

## Error Handling

The component validates all required arguments during initialization. If any required arguments are missing, it will raise a `ValueError` with details about which arguments are missing.

```python
# This will raise a ValueError
try:
    kubeconfig = GKEKubeconfig("invalid", {})
except ValueError as e:
    print(f"Error: {e}")
    # Error: Missing required arguments for GKEKubeconfig: cluster_name, cluster_endpoint, cluster_master_auth. 
    # All of the following arguments are required: cluster_name, cluster_endpoint, cluster_master_auth
```

## Development

### Project Structure

```
gke-kubeconfig/
├── README.md              # This file
├── PulumiPlugin.yaml      # Pulumi plugin configuration
├── requirements.txt       # Python dependencies
├── __main__.py           # Component provider entry point
├── gke_kubeconfig.py     # Main component implementation
└── .gitignore           # Git ignore rules
```

### Running as Component Provider

This component can be run as a Pulumi component provider:

```bash
python __main__.py
```

This starts the component provider host that can be used by Pulumi programs in other languages.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the LumiTorch organization. Please refer to the organization's licensing terms.

## Related Resources

- [Pulumi Component Resources](https://www.pulumi.com/docs/intro/concepts/resources/components/)
- [GKE Authentication](https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl)
- [kubectl Auth Changes in GKE](https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke)
