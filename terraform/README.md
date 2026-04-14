# Cribl as Code - Terraform

Deploy and manage Cribl Cloud packs and worker groups using Terraform.

## Quick Start

```bash
cd examples/install-packs

# Configure credentials
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values

# Initialize and apply
terraform init
terraform plan
terraform apply
```

## Examples

| Example | Description | Use Case |
|---------|-------------|----------|
| [install-packs](examples/install-packs/) | Install packs into existing worker groups | You already have worker groups, want to add packs |
| [create-wg-with-pack](examples/create-wg-with-pack/) | Create a new worker group and install a pack | Starting fresh, need a new worker group |

## Prerequisites

- [Terraform](https://www.terraform.io/downloads) >= 1.0
- Cribl Cloud API credentials (Client ID, Client Secret, Organization ID)
- For `install-packs`: An existing worker group in Cribl Cloud

## Configuration

### Required Variables

| Variable | Description |
|----------|-------------|
| `cribl_client_id` | Cribl Cloud API Client ID |
| `cribl_client_secret` | Cribl Cloud API Client Secret |
| `cribl_cloud_org` | Cribl Cloud Organization ID |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `workspace_id` | Cribl Cloud Workspace ID | `main` |
| `worker_group_name` | Target worker group | `default` |
| `pack_id` | Pack identifier | `cribl-syslog-input` |
| `pack_source` | Pack source URL | GitHub URL |

## Authentication

Use environment variables or `terraform.tfvars`:

```bash
# Environment variables
export TF_VAR_cribl_client_id="your-client-id"
export TF_VAR_cribl_client_secret="your-client-secret"
export TF_VAR_cribl_cloud_org="your-org-id"
```

Or create `terraform.tfvars`:

```hcl
cribl_client_id     = "your-client-id"
cribl_client_secret = "your-client-secret"
cribl_cloud_org     = "your-org-id"
worker_group_name   = "default"
```

## Commit and Deploy

Both examples include `commit_deploy.tf` which automatically:

1. **Commits** configuration changes to Cribl
2. **Gets** the latest config version
3. **Deploys** to the worker group

No manual deployment needed - changes are live after `terraform apply`.

## Pack Sources

Packs can be installed from:

**GitHub:**
```hcl
source = "git+https://github.com/criblpacks/cribl-syslog-input.git"
```

**Pack Dispensary:**
```hcl
source = "https://packs.cribl.io/dl/cribl-aws-bedrock-io/2.0.0/cribl-aws-bedrock-io-2.0.0.crbl"
```

Browse packs at [packs.cribl.io](https://packs.cribl.io)

## Cleanup

```bash
terraform destroy
```

## Resources

- [Cribl Terraform Provider](https://github.com/criblio/terraform-provider-criblio)
- [Terraform Registry](https://registry.terraform.io/providers/criblio/criblio/latest)
- [Cribl Documentation](https://docs.cribl.io)
