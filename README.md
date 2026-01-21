# Cribl as Code Quickstart

A simple, opinionated starting point for managing Cribl Cloud deployments as code. Clone this repo and deploy a worker group with a pack installed in under 30 minutes.

## What This Repo Is For

If you're a Cribl Cloud administrator stuck in ClickOps or struggling with undocumented Terraform, this repo provides clear examples you can clone and extend. Use it as a foundation for:

- Version-controlled Cribl configurations
- Repeatable, automated deployments
- Scalable Day 2 operations

## What You Get

After running either the Terraform or Python quickstart, you'll have:

- A new worker group in your Cribl Cloud organization
- The [AWS VPC Flow Logs pack](https://packs.cribl.io/packs/aws-vpcflow-logs) installed and ready to configure

## Prerequisites

- **Cribl Cloud account** with API credentials ([how to create API credentials](https://docs.cribl.io/stream/api-setup/))
- **Terraform 1.x** (for Terraform quickstart)
- **Python 3.9+** (for Python quickstart)

### Getting Your API Credentials

1. Log into [Cribl Cloud](https://cribl.cloud)
2. Navigate to **Settings > API Credentials**
3. Create a new API credential with appropriate permissions
4. Note your **Client ID**, **Client Secret**, and **Organization ID**

## Quickstart - Terraform

```bash
# Clone the repo
git clone https://github.com/your-org/cribl-as-code-quickstart.git
cd cribl-as-code-quickstart/terraform

# Configure your credentials
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your Cribl Cloud credentials

# Initialize and apply
terraform init
terraform plan
terraform apply
```

After `terraform apply` completes, you'll see output confirming your worker group and pack installation.

## Quickstart - Python SDK

```bash
# Clone the repo
git clone https://github.com/your-org/cribl-as-code-quickstart.git
cd cribl-as-code-quickstart/sdk/python

# Install dependencies
pip install -r requirements.txt

# Configure your credentials
cp .env.example .env
# Edit .env with your Cribl Cloud credentials

# Run the script
python create_wg_with_pack.py
```

## Repo Structure

```
cribl-as-code-quickstart/
├── README.md                           # This file
├── terraform/
│   ├── README.md                       # Terraform-specific documentation
│   ├── provider.tf                     # Provider configuration
│   ├── main.tf                         # Worker group and pack resources
│   ├── variables.tf                    # Input variables
│   ├── outputs.tf                      # Output values
│   ├── terraform.tfvars.example        # Example variable values
│   └── examples/
│       └── create-wg-with-pack/        # Standalone example
└── sdk/
    └── python/
        ├── README.md                   # Python SDK documentation
        ├── requirements.txt            # Python dependencies
        ├── .env.example                # Example environment variables
        └── create_wg_with_pack.py      # Main script
```

## Configuration Options

### Worker Group

| Variable | Description | Default |
|----------|-------------|---------|
| `worker_group_id` | Unique identifier (no spaces) | `quickstart-wg` |
| `worker_group_name` | Display name | `Quickstart Worker Group` |
| `worker_group_description` | Description | `Worker group created via...` |

### Pack

| Variable | Description | Default |
|----------|-------------|---------|
| `pack_id` | Pack identifier | `cribl-aws-vpcflow-logs` |
| `pack_source` | Pack source URL | GitHub URL for AWS VPC Flow Logs |

## Next Steps

After deploying your worker group:

1. **Configure the pack** - Set up sources and destinations for VPC Flow Logs processing
2. **Deploy workers** - Add worker nodes to your new group
3. **Add more packs** - Browse the [Pack Dispensary](https://packs.cribl.io) for additional functionality
4. **Extend your IaC** - Add pipelines, routes, and other configurations

## Resources

- [Cribl Terraform Provider](https://github.com/criblio/terraform-provider-criblio) - Official provider documentation
- [Cribl Python SDK](https://github.com/criblio/cribl_control_plane_sdk_python) - Control Plane SDK
- [Pack Dispensary](https://packs.cribl.io) - Pre-built configuration packs
- [Cribl Documentation](https://docs.cribl.io) - Full product documentation
- [Cribl API Reference](https://docs.cribl.io/stream/api-reference/) - API documentation

## Troubleshooting

### Authentication Errors

- Verify your Client ID and Client Secret are correct
- Ensure your API credentials have sufficient permissions
- Check that your Organization ID matches your Cribl Cloud org

### Worker Group Already Exists

- Change `worker_group_id` to a unique value
- Or delete the existing worker group in Cribl Cloud first

### Pack Installation Fails

- Verify the pack source URL is accessible
- Check that the worker group was created successfully
- Review Cribl Cloud logs for detailed error messages

## License

MIT License - See [LICENSE](LICENSE) for details.
