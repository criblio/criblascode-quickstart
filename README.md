# Cribl as Code Quickstart

A simple, opinionated starting point for Cribl.Cloud admins and platform teams who want to manage Stream as code instead of living in ClickOps. In under 30 minutes, you'll deploy a Worker Group and install a Pack using Terraform or the Python SDK, and have a clean pattern you can extend in your own Git repos.

## What This Repo Is For

If you're a Cribl.Cloud administrator stuck in ClickOps or struggling with undocumented Terraform, this repo provides clear examples you can clone and extend. Use it as a foundation for:

- Version-controlled Cribl configurations
- Repeatable, automated deployments
- Scalable Day 2 operations

## Why GitOps with Cribl

Treating your Cribl configuration like application code means every change is version-controlled, reviewable, and repeatable. Git + Terraform gives you a single place to propose, review, and approve changes to Worker Groups and Packs, instead of relying on one-off UI edits or undocumented scripts. Over time, this makes Day 2 operations like onboarding new sources, rolling out new Packs, and tightening change control a lot less fragile.

## What You Get

After running either the Terraform or Python quickstart, you'll have a baseline Cribl as Code deployment with:

- A new Worker Group in your Cribl.Cloud organization
- A Pack installed and ready to configure
- Automated commit and deploy workflow

## Prerequisites

- **Cribl.Cloud account** with API credentials ([how to create API credentials](https://docs.cribl.io/stream/api-setup/))
- **Terraform 1.x** (for Terraform quickstart)
- **Python 3.9+** (for Python quickstart)

### Getting Your API Credentials

1. Log into [Cribl.Cloud](https://cribl.cloud)
2. Navigate to **Settings > API Credentials**
3. Create a new API credential with appropriate permissions
4. Note your **Client ID**, **Client Secret**, and **Organization ID**

## Run the Terraform Quickstart

Use this path if your team already manages infra with Terraform and you want Cribl.Cloud resources to follow the same review and deployment process.

```bash
# Clone the repo
git clone https://github.com/criblio/criblascode-quickstart.git
cd criblascode-quickstart/terraform/examples/install-packs

# Configure your credentials
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your Cribl.Cloud credentials

# Initialize and apply
terraform init
terraform plan
terraform apply
```

After `terraform apply` completes, your packs are installed and the configuration is automatically committed and deployed to your workers.

## Run the Python SDK Quickstart

Use this path if you prefer a lightweight script or are exploring what's possible with the Cribl SDK before standardizing on Terraform.

```bash
# Clone the repo
git clone https://github.com/criblio/criblascode-quickstart.git
cd criblascode-quickstart/sdk/python

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure your credentials
cp .env.example .env
# Edit .env with your Cribl.Cloud credentials

# Run the script
python create_wg_with_pack.py
```

## Repo Structure

```
criblascode-quickstart/
├── README.md                           # This file
├── terraform/
│   ├── README.md                       # Terraform-specific documentation
│   └── examples/
│       ├── install-packs/              # Quickstart: Install packs into existing worker groups
│       │   ├── main.tf
│       │   ├── variables.tf
│       │   ├── provider.tf
│       │   ├── commit_deploy.tf
│       │   └── terraform.tfvars.example
│       └── create-wg-with-pack/        # Create a new worker group + install pack
└── sdk/
    └── python/
        ├── README.md                   # Python SDK documentation
        ├── config.py                   # Configuration module
        ├── auth.py                     # Authentication module
        ├── worker_groups.py            # Worker group operations
        ├── packs.py                    # Pack operations
        ├── create_wg_with_pack.py      # Main quickstart script
        ├── requirements.txt
        └── .env.example
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
| `pack_source` | Pack Source URL | GitHub URL for AWS VPC Flow Logs |

## Examples

This repo includes standalone examples you can use as templates:

| Example | Description |
|---------|-------------|
| [create-wg-with-pack](terraform/examples/create-wg-with-pack/) | Create a new worker group and install a pack |
| [install-packs](terraform/examples/install-packs/) | Install packs into an existing worker group |

## Next Steps

After you've deployed your Worker Group with the quickstart:

1. **Configure the Pack** - Set up Sources and Destinations for data processing
2. **Deploy Workers** - Add Worker Nodes to your new group
3. **Add more Packs** - Browse the [Pack Dispensary](https://packs.cribl.io) for additional functionality
4. **Extend your IaC** - Add pipelines, routes, and other configurations
5. **Set up CI/CD** - Automate deployments with GitHub Actions or your preferred CI system

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
- Check that your Organization ID matches your Cribl.Cloud org

### Worker Group Already Exists

- Change `worker_group_id` to a unique value
- Or delete the existing Worker Group in Cribl.Cloud first

### Pack Installation Fails

- Verify the pack source URL is accessible
- Check that the Worker Group was created successfully
- Review Cribl.Cloud logs for detailed error messages

### Commit/Deploy Fails

- Ensure the worker group exists and is accessible
- Check that you have deploy permissions for the target group
- Verify there are no conflicting pending changes in the UI

## Security

This repo includes automated security scanning to protect against accidental credential exposure:

- **TruffleHog** - Scans for secrets and credentials
- **Semgrep** - Static analysis for security vulnerabilities
- **tfsec** - Terraform-specific security scanning

### Running Security Scans Locally

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run all checks manually
pre-commit run --all-files
```

### Important Security Notes

- Never commit `.env`, `terraform.tfvars`, or files containing credentials
- Use environment variables or gitignored files for secrets
- Rotate credentials if accidentally exposed

## Contributing

Contributions are welcome! Please ensure your changes pass security scans:

```bash
# Install pre-commit hooks (runs security checks before each commit)
pip install pre-commit
pre-commit install

# Run checks manually
pre-commit run --all-files
```
